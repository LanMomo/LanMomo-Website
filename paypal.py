import paypalrestsdk

from paypalrestsdk import Payment


class Paypal():
    def __init__(self):
        self.return_url = None
        self.cancel_url = None

    def configure(self, client_id, client_secret, mode,
                  return_url, cancel_url):
        paypalrestsdk. \
            configure({
                      "mode": mode,
                      "client_id": client_id,
                      "client_secret": client_secret})
        self.return_url = return_url
        self.cancel_url = cancel_url

    def create(self, ticket):
        price_str = ("%.2f" % ticket.total)

        if ticket.seat_num:
            item_name = "Billet LAN Montmorency 2015 BYOC {}" \
                .format(ticket.seat_num)
        else:
            item_name = "Billet LAN Montmorency 2015 Console"

        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": self.return_url,
                "cancel_url": self.cancel_url
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": item_name,
                        "sku": ("Billet #%d" % ticket.id)
                        "price": price_str,
                        "currency": "CAD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": price_str,
                    "currency": "CAD"
                },
                "description": "Achat de votre billet LAN Montmorency 2015"
            }]
        })

        if payment.create():
            temp_payment = {}

            for link in payment.links:
                if link.method == "REDIRECT":
                    # Convert to str to avoid google appengine unicode issue
                    # https://github.com/paypal/rest-api-sdk-python/pull/58
                    temp_payment['redirect_url'] = str(link.href)

            temp_payment['paypal_payment_id'] = payment['id']
            return temp_payment
        else:
            raise Exception("Erreur lors de la création du paiment: {}"
                            % payment.error)
