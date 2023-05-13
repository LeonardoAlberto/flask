import mercadopago

sdk = mercadopago.SDK("APP_USR-4552254824501886-022223-187f28fb2384d920b7248e90fa71896d-472313762")


def criar_pix(descricao, preco):
    payment_data = {
        "transaction_amount": preco,
        "description": descricao,
        "payment_method_id": "pix",
        "payer": {
            "email": "connect@streaming.com",
            "first_name": "Leonardo",
            "last_name": "Alberto",
            "identification": {
                "type": "CPF",
                "number": "493004898-28"
            },
        }
    }

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]
    return payment
