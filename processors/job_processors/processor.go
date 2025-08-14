package job_processors

import (
	"encoding/json"
	"log"
)

func ProcessJob(body []byte) {

	var jobData JobData

	err := json.Unmarshal(body, &jobData)
	if err != nil {
		log.Printf("Error decoding JSON: %s", err)
		return
	}

	log.Printf("Processing job: %s by %s", jobData.JobTitle, jobData.CompanyName)

}
