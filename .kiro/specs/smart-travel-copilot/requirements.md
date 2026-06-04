# Requirements Document

## Introduction

SmartTravel Copilot is an AI-powered travel decision assistant integrated into the existing SmartTravel application (Next.js frontend + Python FastAPI backend). It guides users through the full trip-planning lifecycle: collecting travel intent, searching and extracting structured travel data, comparing options across multiple dimensions, and recommending the top 3 plans with confidence levels and tradeoff explanations.

The Copilot operates across four decision paths — happy, low-confidence, clarification, and failure — and always presents synthesized, human-readable summaries rather than raw search data dumps.

## Glossary

- **Copilot**: The SmartTravel Copilot AI assistant feature described in this document.
- **Travel Intent**: The structured representation of a user's trip request, composed of destination, duration, budget, and traveler count.
- **Travel Plan**: A ranked, structured recommendation consisting of transport option(s), accommodation option(s), estimated total cost, and itinerary summary.
- **Confidence Score**: A numeric value between 0 and 100 representing the Copilot's certainty that a recommended Travel Plan is a good match for the user's Travel Intent.
- **Clarification Question**: A targeted question the Copilot poses to the user when required Travel Intent fields are missing or ambiguous.
- **Tradeoff Explanation**: A human-readable summary describing how two or more Travel Plans differ across key dimensions (price, duration, comfort, convenience).
- **Failure Recovery Mode**: The operating mode entered when search data is insufficient to produce any Travel Plan recommendation.
- **Search Data**: Results retrieved from internal mock ticket data and/or external web sources (Tavily).
- **Ranking**: The ordered scoring of Travel Plans by the user's chosen priority (price, time, or pickup distance).
- **Agent**: The Python FastAPI backend service (`backend/app/agent/service.py`) that orchestrates search, ranking, and response generation.
- **Chat Interface**: The `ChatAssistant` React component that provides a conversational UI for the Copilot.
- **Results Panel**: The `ResultsList` React component that displays ranked Travel Plans.
- **Clarification Panel**: The `ClarificationPanel` React component that prompts the user for disambiguation.
- **Failure Panel**: The `FailurePanel` React component that displays recovery options when no data is found.
- **Priority**: The user's selected ranking dimension — one of `price`, `time`, or `pickup_distance`.

---

## Requirements

### Requirement 1: Travel Intent Collection

**User Story:** As a traveler, I want the Copilot to collect my destination, travel duration, budget, and number of travelers, so that it has everything it needs to find relevant options before searching.

#### Acceptance Criteria

1. THE Copilot SHALL collect the following required fields before executing a travel search: destination (to_city), origin (from_city), travel date, and traveler count.
2. WHEN a required Travel Intent field is missing from the user's initial request, THE Copilot SHALL ask a Clarification Question for that specific field before proceeding.
3. WHEN all required Travel Intent fields are present, THE Copilot SHALL proceed to search without requesting additional information.
4. WHILE collecting Travel Intent, THE Copilot SHALL accept natural-language input and extract structured field values using normalization.
5. IF the user provides a budget preference, THEN THE Copilot SHALL store it as a Priority signal and apply it during Ranking.
6. THE Copilot SHALL accept city names in both Vietnamese and English aliases (e.g., "Hà Nội", "Ha Noi", "HN") and normalize them to canonical city names.

---

### Requirement 2: Travel Data Search

**User Story:** As a traveler, I want the Copilot to search available travel data automatically after I provide my trip details, so that I receive relevant options without having to search manually.

#### Acceptance Criteria

1. WHEN a complete Travel Intent is available, THE Agent SHALL search the internal mock ticket database for matching transport options.
2. WHEN no internal data matches the Travel Intent, THE Agent SHALL search external web sources via the Tavily API as a fallback.
3. WHILE searching, THE Agent SHALL normalize city names and dates to ensure consistent matching against the internal database.
4. THE Agent SHALL complete the search operation and return a response within 10 seconds under normal network conditions.
5. IF both internal and external search sources return zero results, THEN THE Agent SHALL enter Failure Recovery Mode.
6. WHERE the transport mode is set to a specific value (bus, train, or flight), THE Agent SHALL restrict the internal database search to that transport mode.

---

### Requirement 3: Travel Information Extraction and Structuring

**User Story:** As a traveler, I want the Copilot to extract structured information from raw search results, so that I can compare options clearly without reading through unformatted data.

#### Acceptance Criteria

1. WHEN external web search results are available, THE Agent SHALL extract structured ticket information (provider, price, departure time, pickup point) from raw Tavily content using the LLM.
2. THE Agent SHALL present all search results as structured Travel Plans, never as raw unformatted text dumps.
3. WHEN the LLM extraction step fails or is unavailable, THE Agent SHALL fall back to a formatted list of source titles and URLs.
4. THE Agent SHALL include a `rank_reason` field in every Travel Plan explaining why it was selected or ranked at its position.
5. FOR ALL Travel Plans derived from internal data, THE Agent SHALL generate booking deep-links and Google Maps links for each pickup point.

---

### Requirement 4: Travel Options Comparison

**User Story:** As a traveler, I want the Copilot to compare travel options across price, travel time, and pickup convenience, so that I can make an informed decision based on what matters most to me.

#### Acceptance Criteria

1. THE Agent SHALL compare available transport options along at minimum three dimensions: price (VND), departure time, and pickup distance (km from user location).
2. WHEN the user selects a Priority, THE Agent SHALL re-rank all available Travel Plans according to that Priority without repeating the data search.
3. THE Results Panel SHALL display a Tradeoff Explanation for each Travel Plan describing its rank reason relative to the user's chosen Priority.
4. THE Copilot SHALL surface a maximum of 3 Travel Plans in any single response, ranked by the active Priority.
5. WHILE displaying comparison results, THE Results Panel SHALL visually differentiate the top-ranked plan from lower-ranked alternatives.

---

### Requirement 5: Top 3 Travel Plan Recommendation

**User Story:** As a traveler, I want the Copilot to recommend the top 3 travel plans with clear explanations, so that I have meaningful choices without being overwhelmed.

#### Acceptance Criteria

1. WHEN ranked Travel Plans are available, THE Results Panel SHALL display exactly the top 3 plans ordered by the active Priority.
2. THE Copilot SHALL include a plain-language summary sentence above the ranked list describing the search outcome (e.g., number of options found, active priority).
3. WHEN fewer than 3 Travel Plans are available, THE Results Panel SHALL display all available plans and note in the summary that fewer options were found.
4. WHEN only 1 Travel Plan is available, THE Copilot SHALL set the path to `low_confidence` and include a warning explaining the limited choice.
5. THE Agent SHALL include a `summary` field in every response that describes the result in one or two human-readable sentences.

---

### Requirement 6: Tradeoff Explanation

**User Story:** As a traveler, I want the Copilot to explain the tradeoffs between the recommended options, so that I understand what I am giving up or gaining with each choice.

#### Acceptance Criteria

1. THE Agent SHALL generate a `rank_reason` string for each Travel Plan that explicitly states why it ranks at its position given the active Priority.
2. WHEN the active Priority is `price`, THE Agent SHALL state the price advantage or disadvantage of each plan relative to the cheapest option.
3. WHEN the active Priority is `time`, THE Agent SHALL state the departure time and explain whether it is the earliest, mid-range, or latest available departure.
4. WHEN the active Priority is `pickup_distance`, THE Agent SHALL state the distance in km from the user's location and compare it to alternatives.
5. THE Results Panel SHALL render the `rank_reason` field visibly on each Travel Plan card.

---

### Requirement 7: Confidence Levels

**User Story:** As a traveler, I want to see confidence levels for each recommendation, so that I know how reliable the suggestions are before booking.

#### Acceptance Criteria

1. THE Agent SHALL assign a Confidence Score (0–100) to each response based on data completeness and match quality.
2. WHEN all required Travel Intent fields are matched by at least one internal data record, THE Agent SHALL assign a Confidence Score of 80 or above.
3. WHEN results come exclusively from external web sources, THE Agent SHALL assign a Confidence Score below 60 and set the path to `low_confidence`.
4. WHEN only one Travel Plan is found for a given Travel Intent, THE Agent SHALL assign a Confidence Score below 70.
5. THE Results Panel SHALL display the Confidence Score alongside the path status badge for each search result.
6. IF the Confidence Score is below 60, THEN THE Copilot SHALL display a visible warning message explaining why confidence is limited.

---

### Requirement 8: Clarification Questions

**User Story:** As a traveler, I want the Copilot to ask me targeted clarification questions when it is unsure about my intent, so that it does not make incorrect assumptions that lead to wrong recommendations.

#### Acceptance Criteria

1. WHEN an ambiguous pickup location is detected (e.g., "Thanh Phong"), THE Agent SHALL set the path to `clarification` and return a `clarification_question` and `clarification_options`.
2. THE Clarification Panel SHALL display the `clarification_question` text and render one button per `clarification_option`.
3. WHEN the user selects a clarification option, THE Agent SHALL re-execute the search with the resolved intent and return a new response.
4. WHEN a required Travel Intent field cannot be inferred from the user's message, THE Chat Interface SHALL prompt the user for that specific field before triggering a backend search.
5. THE Copilot SHALL ask no more than one Clarification Question per interaction turn to avoid overwhelming the user.
6. IF the Confidence Score is below 50, THEN THE Copilot SHALL proactively ask one follow-up clarification question to improve result quality.

---

### Requirement 9: Failure Recovery Mode

**User Story:** As a traveler, I want the Copilot to guide me toward useful alternatives when my search returns no results, so that I am not left with a dead end.

#### Acceptance Criteria

1. WHEN both internal and external searches return zero results, THE Agent SHALL enter Failure Recovery Mode and set the path to `failure`.
2. WHILE in Failure Recovery Mode, THE Agent SHALL suggest up to 3 nearby alternative dates that have known data in the internal database.
3. WHEN in Failure Recovery Mode, THE Failure Panel SHALL display the failure `summary`, an optional `warning`, and all `suggested_dates` as clickable buttons.
4. WHEN the user clicks a suggested date, THE Copilot SHALL re-execute the search with that date and exit Failure Recovery Mode if results are found.
5. IF the Tavily API key is missing or the Tavily request times out, THEN THE Agent SHALL treat the external search as returning zero results and proceed with the failure or fallback logic accordingly.
6. WHILE in Failure Recovery Mode, THE Copilot SHALL never display an empty results area without a recovery action or explanation.

---

### Requirement 10: Search Result Summarization

**User Story:** As a traveler, I want the Copilot to always summarize findings in plain language rather than dumping raw data, so that I can understand the results quickly.

#### Acceptance Criteria

1. THE Agent SHALL include a plain-language `summary` string in every API response, regardless of the response path.
2. WHEN external web search results are present, THE Agent SHALL use the LLM to extract structured information and produce a synthesized summary rather than returning raw Tavily content.
3. THE Results Panel SHALL render the `summary` field as the first visible text element in the results view.
4. THE Chat Interface SHALL never display raw JSON, raw API payloads, or unformatted search engine output to the user.
5. WHEN the LLM extraction step is unavailable, THE Agent SHALL generate a fallback summary from the available source titles using a formatted bullet list.
6. FOR ALL responses where travel options are found, THE Agent SHALL include the count of options, the active Priority, and the route (from_city → to_city) in the `summary` string.

---

### Requirement 11: Parser and Data Normalization (Round-Trip)

**User Story:** As a developer, I want city names and dates to be normalized consistently through parsing and formatting, so that the search logic produces correct matches regardless of the input format the user provides.

#### Acceptance Criteria

1. WHEN a city name is provided in any supported alias form, THE Normalizer SHALL convert it to its canonical form (e.g., "HN" → "Ha Noi", "Sài Gòn" → "Ho Chi Minh").
2. WHEN a date string is provided in any supported format (YYYY-MM-DD, DD/MM/YYYY, D/M), THE Normalizer SHALL parse it into a canonical YYYY-MM-DD string.
3. THE Normalizer SHALL format canonical city names back into display-friendly Vietnamese labels for use in the UI.
4. FOR ALL valid canonical city names, normalizing then formatting then normalizing SHALL produce the same canonical value (round-trip property).
5. IF an unrecognized city alias is provided, THEN THE Normalizer SHALL return the input unchanged and log a warning.
6. IF an unparseable date string is provided, THEN THE Normalizer SHALL fall back to the default date (2026-06-06) and log a warning.
