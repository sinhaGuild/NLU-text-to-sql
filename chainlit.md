# Text-to-SQL Execution
Enterprise data is often stored in SQL databases.
LLMs make it possible to interact with SQL databases using natural language. We can essentially build SQL `Chains` and Agents to build and run SQL queries based on natural language prompts. These are compatible with any SQL dialect supported by SQLAlchemy (e.g., MySQL, PostgreSQL, Oracle SQL, Databricks, SQLite).
![Alt text](./public/image.png)

## Target Use Cases

- Generating queries that will be run based on natural language questions
- Building custom dashboards based on insights a user wants to analyze
- Creating chatbots that can answer questions based on database data
- Generating complex queries based on natural language
- Expanding database access to non-technical people and stakeholders

## Benefits
- Business users can access organisational data in a direct and timely way.
- This relieves data scientists and analysts from the burden of ad-hoc requests from business users and allows them to focus on advanced data challenges.
- The business can leverage its data in a more fluid and strategic way, finally turning it into a solid basis for decision making.

## Workflow
- Build SQL queries based on natural language user questions
- Query a SQL database using chains for query creation and execution
- Interact with a SQL database using agents for robust and flexible querying

![Alt text](./public/workflow.png)

## Example
The repo uses a sample database curated for learning purposes and has the tables
`['albums', 'artists', 'customers', 'employees', 'genres', 'invoice_items', 'invoices', 'media_types', 'playlist_track', 'playlists', 'tracks']`

### Sample Questions
- Describe Tables
  `Describe the playlisttrack table?`
- Describe and recover from errors.
  `Describe the playlistsong table`
- Complex queries
  `List the total sales per country. Which country's customers spent the most?`
  `Show the total number of tracks in each playlist. The Playlist name should be included in the result.`
- Complex queries, recovering from error
  `Who are the top 3 best selling artists?`