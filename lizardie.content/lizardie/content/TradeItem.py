import sys

class TradeItem:
    """
    Trade item
    """
    def __init__(self, n, auction, nlot, lot, startPrice, organizer, applicationEndDate, date, state, winner):
        self.n = n[0] # item number
        self.n_link = n[1]
        self.auction = auction[0].strip()
        self.auction_link = auction[1]
        self.nlot = nlot[0] # lot number
        self.nlot_link = nlot[1]
        self.lot = lot[0].strip()
        self.lot_link = lot[1]
        self.startPrice = startPrice[0].strip() # na4alnaja cena
        self.organizer = organizer[0].strip() # organizator torgov
        self.organizer_link = organizer[1]
        self.applicationEndDate = applicationEndDate[0].strip() # data okon4anija predstavlenija zajavok
        self.date = date[0].strip() # data provedenija
        self.state = state[0].strip()
        self.winner = winner[0]

#    def __init__(self, data):
#        return self.__init__(self, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9])

    def Print(self, f=sys.stdout):
        """Prints the item in the f descriptor"""
        print>>f, ""
        print>>f, "Item number:", self.n.encode('utf8')
        print>>f, "Auction:", self.auction.encode('utf8')
        print>>f, "Lot number:", self.nlot.encode('utf8')
        print>>f, "Lot:", self.lot.encode('utf8')
        print>>f, "Start price:", self.startPrice.encode('utf8')
        print>>f, "Organizer:", self.organizer.encode('utf8')
        print>>f, "Application end date:", self.applicationEndDate.encode('utf8')
        print>>f, "Auction date:", self.date.encode('utf8')
        print>>f, "State:", self.state.encode('utf8')
        print>>f, "Winner:", 
        if self.winner: print>>f, self.winner.encode('utf8')
        else: print>>f, ""
