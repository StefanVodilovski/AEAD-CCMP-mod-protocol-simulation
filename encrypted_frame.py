class Encrypted_frame:
    def __init__(self, sourceAddress, destinationAddress, data, mic, pn=0, fcs=0):
        self.sourceAdress = sourceAddress
        self.destinationAdress = destinationAddress
        self.pn = pn
        self.data = data
        self.mic = mic
        self.fcs = fcs

    def get_encrypted_data(self):
        return self.data

    def get_encrypted_source_addr(self):
        return self.sourceAdress

    def get_encrypted_destination_addr(self):
        return self.destinationAdress

    def get_mic(self):
        return self.mic
