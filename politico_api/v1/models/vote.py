votes = {

}

class  VoteModel:
    def __init__(self, voter_info=None, candidate_info=None, position=None):
        self.voter_info = voter_info
        self.candidate_info = candidate_info
        self.position = position
    
    def insert_vote(self):

        for vote in votes:
            if votes[vote]["voter_info"] == self.voter_info and votes[vote]["position"] == self.position:
                return None 

        id = len(votes) + 1
        
        vote_info = {
            "id": id, 
            "voter_info": self.voter_info,
            "candidate_info": self.candidate_info,
            "position": self.position
        }

        votes[id] = vote_info
        return True
    
    def get_all_votes(self):
        all_votes = []
        for vote in votes:
            all_votes.append(votes[vote])
        return all_votes
    
    
