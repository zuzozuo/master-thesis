package mysender

import (
	"context"
	myutils "learning/myutils"
	"log"
	"strconv"
	"time"

	consts "learning/configs"

	amqp "github.com/rabbitmq/amqp091-go"
)

func MySend() {

	conn, err := amqp.Dial("amqp://" + consts.USERNAME + ":" + consts.PASSWORD + "@" + consts.CONN_STRING + ":" + strconv.Itoa(consts.CONN_PORT) + "/")

	myutils.FailOnError(err, "Failed to connect to RabbitMQ")

	ch, err := conn.Channel()
	myutils.FailOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"hello", // name
		false,   // durable
		false,   // delete when unused
		false,   // exclusive
		false,   // no-wait
		nil,     // arguments
	)
	myutils.FailOnError(err, "Failed to declare a queue")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	body := "Hello World!"
	err = ch.PublishWithContext(ctx,
		"",     // exchange
		q.Name, // routing key
		false,  // mandatory
		false,  // immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(body),
		})
	myutils.FailOnError(err, "Failed to publish a message")
	log.Printf(" [x] Sent %s\n", body)

	defer conn.Close()

}
