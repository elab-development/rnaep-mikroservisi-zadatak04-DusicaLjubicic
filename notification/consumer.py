import os
import time
from dotenv import load_dotenv
from redis_om import get_redis_connection

load_dotenv()

redis = get_redis_connection(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", ""),
    decode_responses=True
)

# Ovaj servis slusa dva stream-a: order_completed i refund_order
streams = {
    'order_completed': 'notification-completed-group',
    'refund_order': 'notification-refund-group',
}

# Kreiramo consumer grupe za oba stream-a
for stream_key, group_name in streams.items():
    try:
        redis.xgroup_create(stream_key, group_name, id='0', mkstream=True)
        print(f"Kreirana grupa '{group_name}' za stream '{stream_key}'")
    except Exception:
        # Grupa vec postoji - resetuj da cita od pocetka
        redis.xgroup_setid(stream_key, group_name, '0')
        print(f"Grupa '{group_name}' resetovana da cita od pocetka.")

print("Notification servis pokrenut. Cekam dogadjaje...")

while True:
    try:
        for stream_key, group_name in streams.items():
            results = redis.xreadgroup(
                group_name,
                'notification-consumer',
                {stream_key: '>'},
                count=10,
                block=1000
            )

            if results:
                for stream, messages in results:
                    for message_id, data in messages:
                        order_id = data.get('pk', data.get('id', 'nepoznat'))

                        if stream_key == 'order_completed':
                            print(f"Obavestenje: Porudzbina {order_id} je uspesno kreirana i placena.")
                        elif stream_key == 'refund_order':
                            print(f"Obavestenje: Porudzbina {order_id} je refundirana.")

                        redis.xack(stream_key, group_name, message_id)

    except Exception as e:
        print(f"Greska u notification consumer-u: {e}")

    time.sleep(1)
