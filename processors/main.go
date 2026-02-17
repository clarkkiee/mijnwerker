package main

import (
	"log"
	"os"
	"os/signal"
	"syscall"

	"github.com/clarkkiee/mijnwerker/job_processors"
	amqp "github.com/rabbitmq/amqp091-go"
)

func main() {

	rabbitmqHost := os.Getenv("RABBITMQ_HOST")
	if rabbitmqHost == "" {
		rabbitmqHost = "localhost"
	}

	conn, err := amqp.Dial("amqp://guest:guest@" + rabbitmqHost + ":5672/")
	if err != nil {
		log.Fatalf("Failed to connect to RabbitMQ: %s", err)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("Failed to initiate channel: %s", err)
	}
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"job_queue",
		false,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		log.Fatalf("Failed to declare a queue: %s", err)
	}

	msgs, err := ch.Consume(
		q.Name,
		"",
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		log.Fatalf("Failed to register a consumer: %s", err)
	}

	go func() {
		for d := range msgs {
			go job_processors.ProcessJob(d.Body)
		}
	}()

	log.Printf(" [*] Waiting for messages. To exit, press CTRL+C")
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	<- sigs

}