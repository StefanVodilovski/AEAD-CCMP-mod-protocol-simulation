class Clear_Text_frame:
    def __init__(self, data="", source_address="", destination_address="", pn=0):
        self.data = data
        self.source_address = source_address
        self.destination_adress = destination_address
        self.pn = pn

    def set_data(self, data):
        self.data = data

    def set_source_address(self, source_address):
        self.source_address = source_address

    def set_destination_address(self, destination_address):
        self.destination_adress = destination_address

    def get_source_addr(self):
        return self.source_address

    def get_dest_addr(self):
        return self.destination_adress

    def get_payload(self):
        return self.data
