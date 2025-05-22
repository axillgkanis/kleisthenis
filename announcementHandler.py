from dbManager import dbManager

class annoucementHandler:
    def __init__(self, announcement):
        self.announcement = announcement

    def searchAnnouncement(self):
        return dbManager.query_announcements()    
    
    def newAnnouncement(self):
        return dbManager.insert_announcement(self.announcement['title'], self.announcement['body'])
    
    def editAnnouncement(self):
        return dbManager.modify_announcement(self.announcement['id'], self.announcement['title'], self.announcement['body'])
    
    def deleteAnnouncement(self):
        return dbManager.delete_announcement(self.announcement['id'])
    
    def createCancelledMeetingAnnouncement(self):
        #TODO
        return
    
    def createResultsAnnouncement(self):
        #TODO
        return