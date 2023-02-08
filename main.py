import pandas as pd

df = pd.read_csv('hotels.csv', dtype={'id': str})
df_cards = pd.read_csv('cards.csv', dtype=str).to_dict(orient='records')
df_security = pd.read_csv('card_security.csv', dtype=str)

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df['id'] == self.hotel_id, 'name'].squeeze()

    def book(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df['id'] == self.hotel_id, 'available'] = 'no'
        df.to_csv('hotels.csv', index=False)

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df['id'] == self.hotel_id, 'available'].squeeze()
        if availability == 'yes':
            return True
        else:
            return False


class SpaHotel(Hotel):
    def book_spa_package(self):
        pass

class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here are your booking data:
        Name: {self.customer}
        Hotel name: {self.hotel.name}
        """
        return content


class SpaTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your SPA reservation!
        Here are your SPA booking data:
        Name: {self.customer}
        Hotel name: {self.hotel.name}
        """
        return content

class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {'number': self.number, 'expiration': expiration,
                     'holder': holder, 'cvc': cvc}
        if card_data in df_cards:
            return True
        else:
            return False

class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_security.loc[df_security['number'] == self.number, 'password'].squeeze()
        if password == given_password:
            return True
        else:
            return False


print(df)
hotel_id = input('Enter the id of the hotel: ')
hotel = SpaHotel(hotel_id)

if hotel.available():
    credit_card = SecureCreditCard("1234")
    if credit_card.validate("12/26", "JOHN SMITH", "123"):
        if credit_card.authenticate('mypass'):
            hotel.book()
            name = input('Please enter your name: ')
            reservation_ticket = ReservationTicket(name, hotel)
            print(reservation_ticket.generate())
            spa = input('Would you like to book SPA package: ')
            if spa.lower() == 'yes' or 'y':
                hotel.book_spa_package()
                spa_ticket = SpaTicket(name, hotel)
                print(spa_ticket.generate())
        else:
            print('Credit card authentication failed')
    else:
        print('There is a problem with your payment')
else:
    print('The hotel is not available')

