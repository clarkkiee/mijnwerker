package job_processors

type JobData struct {
	JobTitle      string   `json:"job_title"`
	CompanyName   string   `json:"company_name"`
	JobType       string   `json:"job_type"`
	WorkplaceType string   `json:"workplace_type"`
	JobLocation   string   `json:"job_location"`
	Descriptions  []string `json:"descriptions"`
	Requirements  []string `json:"requirements"`
}
