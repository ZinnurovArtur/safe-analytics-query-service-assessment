# Research Software Engineer Take Home Assessment

## Safe Analytics Query Service

You are building a lightweight analytics service that allows users to query aggregate information from datasets in a safe and reproducible way.

The service should:

- Load structured data from CSV
- Expose a simple API
- Return aggregate statistics
- Apply configurable safety rules
- Generate audit logs

---

# Objective

The goal of this exercise is to assess practical software engineering, API design, testing, validation logic, and problem solving skills.

We are more interested in your engineering decisions, code quality, reasoning, and approach than production ready completeness. We don't expect a production grade implementation.  A clean and well reasoned solution is preferred over excessive features.

---

# Requirements

## 1. Load a Dataset

Your application should load the CSV dataset provided in:

```text
data/employees.csv
```

You may use any language or framework.

---

## 2. Expose an API

Create an API endpoint that allows querying aggregate statistics.

Example:

```http
POST /query
```

Example request:

```json
{
  "group_by": "department"
}
```

---

## 3. Apply Safety Rules

Results with counts below the suppression threshold should be suppressed.

For this exercise, assume a default suppression threshold of `3`.

Example:

```json
{
  "Executive": "suppressed"
}
```

---

## 4. Support Filtering

Support simple filtering in queries.

Example:

```json
{
  "group_by": "department",
  "filter": {
    "location": "London"
  }
}
```

---

## 5. Generate Audit Logs

Each query should generate an audit log entry containing:

- timestamp
- query details
- whether suppression was triggered

Example:

```json
{
  "timestamp": "2026-05-26T10:00:00Z",
  "group_by": "department",
  "filters": {
    "location": "London"
  },
  "suppression_triggered": true
}
```

---

## 6. Containerise the Application

Please provide:

- Dockerfile
- simple run instructions

---

## 7. Include Basic Tests

Please include a few tests where appropriate.

Examples:

- validation logic
- suppression behaviour
- API responses
- filtering behaviour

---

# Dataset

Dataset file:

```text
data/employees.csv
```

# Example Scenarios

## Example 1: Standard Aggregation

Request:

```bash
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{
    "group_by": "department"
  }'
```

Expected response:

```json
{
  "Engineering": 9,
  "Finance": 3,
  "HR": 3,
  "Marketing": 3,
  "Support": 3,
  "Research": 4,
  "Legal": 3,
  "Executive": "suppressed"
}
```

Explanation:

Records are aggregated by department and returned as counts. Departments with counts greater than or equal to the suppression threshold are returned normally.

Departments below the suppression threshold are suppressed to reduce the risk of exposing sensitive or identifiable information.

---

## Example 2: Filtering and Suppression Scenario

Request:

```bash
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{
    "group_by": "department",
    "filter": {
      "location": "Manchester"
    }
  }'
```

Expected response:

```json
{
  "Engineering": "suppressed",
  "Finance": "suppressed",
  "Marketing": "suppressed",
  "HR": "suppressed",
  "Research": "suppressed",
  "Support": "suppressed",
  "Legal": "suppressed",
  "Executive": "suppressed"
}
```

Explanation:

The dataset is first filtered to include only employees located in Manchester. The remaining records are then grouped by department.

Because each department contains fewer than the suppression threshold number of records after filtering, all results are suppressed.

---

## Example 3: Invalid Column

Request:

```bash
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{
    "group_by": "unknown_column"
  }'
```

Expected response:

```json
{
  "error": "Invalid group_by field: unknown_column"
}
```

Explanation:

The request attempts to group by a column that does not exist in the dataset.

The service should validate incoming requests and return a clear validation error instead of failing unexpectedly.

---

# Submission Instructions

Please fork this repository and implement your solution in your own fork.

Once completed, please share the GitHub repository link as your submission.

Please include:

- source code
- README updates if required
- Dockerfile
- tests
- run instructions

---

# Notes

You are free to make reasonable assumptions where requirements are ambiguous.

Please document any assumptions clearly in the README.

---

# Running the Application

## Prerequisites

- Python 3.12+
- Docker (for containerised run)

---

## Option 1: Local

**Install dependencies:**

```bash
pip install -r requirements/requirements.txt
```

**Configure environment** (copy the example and adjust if needed):

```bash
cp src/.env.example src/.env
```

Potentially use the relative file path of files:

For example:

```bash
CSV_PATH=../data/employees.csv
```

**Start the server:**

```bash
cd src
uvicorn main:app --host 0.0.0.0 --port 8080
```

---

## Option 2: Docker

**Build the image** (run from the repo root):

```bash
docker build -f docker/Dockerfile -t safe-analytics-query-service .
```

**Run the container:**

```bash
docker run --env-file src/.env -p 8080:8080 safe-analytics-query-service
```

Override any variable inline if needed:

Use the `.env.example` to have an `.env` file for docker run

```bash
docker run --env-file src/.env -e SUPPRESSION_THRESHOLD=5 -p 8080:8080 safe-analytics-query-service
```

The API is available at `http://localhost:8080`. Interactive docs at `http://localhost:8080/docs`.

---

## Running Tests

```bash
pip install -r requirements/test.txt
pytest
```

---

# Assumptions

- Assuming we will use the data in the csv. In the future the case-sensitivity needs to be implemented. 
- Suppression applies to group counts — a group whose count is strictly less than the threshold (`< 3` by default) is returned as `"suppressed"`.
- The suppression threshold can be overridden by setting the `SUPPRESSION_THRESHOLD` environment variable.
- Filter values are strings only (v1). Numeric or range-based filters are out of scope.
- I have added the restriction on the identifiable fields to prevent leak of sensitive information
- No authentication is required

# Future work

- Implementing the /audit query to see the audits
- Add the database for performing extensive analysis for the audits
- Adding the CI/CD pipeline for tests
- Understand if we need to have an proper UX response if no data
- Using numpy/pandas for the extensive calculations

