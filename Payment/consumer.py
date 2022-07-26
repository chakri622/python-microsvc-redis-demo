from main import redis, Order
import time

key= 'refund_order'
group= 'payment-group'

try:
    redis.xgroup_create(key, group)
except:
    print("Group already exists!")

while True:
    try:
        print("Reading from group")
        results = redis.xreadgroup(group, key, {key: '>'}, None)
        print(results)
        if results != []:
            for result in results:
                obj = result[1][0][1]
                order = Order.get(obj['pk'])
                order.status = 'refunded'
                order.save()

        #print(results)

    except Exception as e:
        print("In Exception")
        print(str(e))

    time.sleep(1)

