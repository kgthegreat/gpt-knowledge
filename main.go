package main

import (
	"fmt"
	"os"
	"time"
	"github.com/joho/godotenv"
	"github.com/rusq/slackdump"
	"log"
)

func fetchSlackMessages(channelID, fromDate, toDate string) error {
	// Load environment variables from .env file
	err := godotenv.Load()
	if err != nil {
		return fmt.Errorf("error loading .env file: %v", err)
	}

	// Get the organization from environment variables
	org := os.Getenv("SLACK_ORG")
	if org == "" {
		org = "skyscanner" // default organization
	}

	// Convert dates to time.Time
	from, err := time.Parse("2006-01-02", fromDate)
	if err != nil {
		return fmt.Errorf("invalid from-date format: %v", err)
	}

	to, err := time.Parse("2006-01-02", toDate)
	if err != nil {
		return fmt.Errorf("invalid to-date format: %v", err)
	}

	// Use slackdump to fetch messages
	// This is a placeholder for the actual slackdump usage
	fmt.Printf("Fetching messages from channel %s in org %s from %s to %s\n", channelID, org, from, to)
	// Implement the actual slackdump logic here

	return nil
}

func main() {
	if len(os.Args) < 5 || os.Args[1] != "fetch-slack" {
		log.Fatalf("Usage: %s fetch-slack <channel-id> <from-date> <to-date>", os.Args[0])
	}

	channelID := os.Args[2]
	fromDate := os.Args[3]
	toDate := os.Args[4]

	err := fetchSlackMessages(channelID, fromDate, toDate)
	if err != nil {
		log.Fatalf("Error fetching Slack messages: %v", err)
	}
}
