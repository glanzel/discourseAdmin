class Utils():
    def getDiscourseClient():
        return DiscourseClient(
            'http://localhost:3000',
            api_username='system',
            api_key='84531905176dfd5d7cde45008430f879da00e43a94510cd39d540bd13d1d01b1')
