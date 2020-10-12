class event:
    def __init__(
        self, name="", description="", sign_up_url="", occurrences=[]
    ):
        self.name = name
        self.description = description
        self.sign_up_url = sign_up_url
        self.occurrences = occurrences

    def get_date_time_strings(self):
        return_list = []
        for occ in self.occurrences:
            return_list.append(
                occ.strftime("%A, %B %-d (%m/%d/%Y) at %-I:%M %p")
            )
        return return_list
