import pika
from scrapers import dealls

def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='job_queue')
        
        dealls.scrape(channel)
        
    except pika.exceptions.AMQPConnectionError as e:
        print(f"failed connect to RabbitMQ: {e}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()
        
        
if __name__ == '__main__':
    main()