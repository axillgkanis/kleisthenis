import hashlib
import time
import json
from typing import List, Dict, Any, Optional


class Block:
    def __init__(self, index: int, timestamp: float, data: Dict[str, Any], previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calculate the hash of the block."""
        block_string = json.dumps(
            {"index": self.index, "timestamp": self.timestamp,
             "data": self.data, "previous_hash": self.previous_hash,
             "nonce": self.nonce}, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        """Simple proof of work algorithm."""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()


class TopicBlock(Block):
    def __init__(self, index: int, topic_id: str, title: str, description: str,
                 options: List[str], previous_hash: str):
        data = {
            "block_type": "topic",
            "topic_id": topic_id,
            "title": title,
            "description": description,
            "options": options
        }
        super().__init__(index, time.time(), data, previous_hash)


class VoteBlock(Block):
    def __init__(self, index: int, topic_id: str, voter_id: str, vote_choice: str, previous_hash: str):
        data = {
            "block_type": "vote",
            "topic_id": topic_id,
            "voter_id": voter_id,
            "vote_choice": vote_choice
        }
        super().__init__(index, time.time(), data, previous_hash)


class Blockchain:
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """Create the first block in the chain."""
        genesis_block = Block(
            0, time.time(), {"block_type": "genesis", "message": "Genesis Block"}, "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """Get the latest block in the blockchain."""
        return self.chain[-1]

    def add_topic_block(self, topic_id: str, title: str, description: str, options: List[str]) -> TopicBlock:
        """Add a new topic block to the blockchain."""
        latest_block = self.get_latest_block()
        new_block = TopicBlock(
            len(self.chain), topic_id, title, description, options, latest_block.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block

    def add_vote_block(self, topic_id: str, voter_id: str, vote_choice: str) -> Optional[VoteBlock]:
        """Add a new vote block to the blockchain."""
        # Verify topic exists
        topic_exists = any(
            block.data.get("block_type") == "topic" and block.data.get(
                "topic_id") == topic_id
            for block in self.chain
        )

        if not topic_exists:
            print(f"Topic {topic_id} does not exist.")
            return None

        latest_block = self.get_latest_block()
        new_block = VoteBlock(
            len(self.chain), topic_id, voter_id, vote_choice, latest_block.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        """Check if the blockchain is valid."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Verify current block's hash
            if current_block.hash != current_block.calculate_hash():
                return False

            # Verify chain link
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_votes(self, topic_id: str) -> Dict[str, int]:
        """Get vote counts for a specific topic."""
        votes = {}

        # First check if topic exists
        topic_exists = any(
            block.data.get("block_type") == "topic" and block.data.get(
                "topic_id") == topic_id
            for block in self.chain
        )

        if not topic_exists:
            print(f"Topic {topic_id} does not exist.")
            return votes

        for block in self.chain:
            if (block.data.get("block_type") == "vote" and
                    block.data.get("topic_id") == topic_id):
                vote_choice = block.data.get("vote_choice")
                votes[vote_choice] = votes.get(vote_choice, 0) + 1

        return votes

    def save_to_file(self, filename: str = "blockchain.json") -> None:
        """Save blockchain to a JSON file."""
        # Convert the blockchain to a serializable format
        serializable_chain = []
        for block in self.chain:
            serializable_block = {
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "previous_hash": block.previous_hash,
                "nonce": block.nonce,
                "hash": block.hash
            }
            serializable_chain.append(serializable_block)

        # Write to file
        with open(filename, 'w') as file:
            json.dump({
                "chain": serializable_chain,
                "difficulty": self.difficulty
            }, file, indent=4)
        print(f"Blockchain saved to {filename}")

    @classmethod
    def load_from_file(cls, filename: str = "blockchain.json") -> 'Blockchain':
        """Load blockchain from a JSON file."""
        try:
            with open(filename, 'r') as file:
                data = json.load(file)

            blockchain = cls(difficulty=data["difficulty"])
            # Remove genesis block that was created in __init__
            blockchain.chain = []

            # Reconstruct each block
            for block_data in data["chain"]:
                if block_data["data"]["block_type"] == "topic":
                    block = TopicBlock(
                        block_data["index"],
                        block_data["data"]["topic_id"],
                        block_data["data"]["title"],
                        block_data["data"]["description"],
                        block_data["data"]["options"],
                        block_data["previous_hash"]
                    )
                elif block_data["data"]["block_type"] == "vote":
                    block = VoteBlock(
                        block_data["index"],
                        block_data["data"]["topic_id"],
                        block_data["data"]["voter_id"],
                        block_data["data"]["vote_choice"],
                        block_data["previous_hash"]
                    )
                else:  # Genesis or other types
                    block = Block(
                        block_data["index"],
                        block_data["timestamp"],
                        block_data["data"],
                        block_data["previous_hash"]
                    )

                # Restore the hash and nonce instead of recalculating
                block.nonce = block_data["nonce"]
                block.hash = block_data["hash"]
                blockchain.chain.append(block)

            return blockchain
        except FileNotFoundError:
            print(f"File {filename} not found. Creating a new blockchain.")
            return cls()


# Example usage
if __name__ == "__main__":
    # Try to load existing chain or create new one
    voting_chain = Blockchain.load_from_file()

    # Add a topic if the chain is new
    if len(voting_chain.chain) <= 1:  # Only genesis block
        voting_chain.add_topic_block(
            "topic-1",
            "Best Programming Language",
            "Vote for your favorite programming language",
            ["Python", "JavaScript", "Java", "C++", "Go"]
        )

    # Add some votes
    voting_chain.add_vote_block(
        "topic-1", f"voter-{int(time.time())}", "Python")

    # Check results
    print("Vote results:", voting_chain.get_votes_for_topic("topic-1"))
    print("Is blockchain valid?", voting_chain.is_chain_valid())

    # Save the blockchain
    voting_chain.save_to_file()
