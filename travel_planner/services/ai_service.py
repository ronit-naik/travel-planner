import asyncio
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from ..config import initialize_llm, logger


async def get_ai_recommendation(data_type, formatted_data):
    logger.info(f"Getting {data_type} analysis from AI")
    llm_model = initialize_llm()

    # Configure agent based on data type
    if data_type == "flights":
        role = "AI Flight Analyst"
        goal = "Analyze flight options and recommend the best one considering price, duration, stops, and overall convenience."
        backstory = f"AI expert that provides in-depth analysis comparing flight options based on multiple factors."
        description = """
        Recommend the best flight from the available options, based on the details provided below:

        **Reasoning for Recommendation:**
        - **Price:** Provide a detailed explanation about why this flight offers the best value compared to others.
        - **Duration:** Explain why this flight has the best duration in comparison to others.
        - **Stops:** Discuss why this flight has minimal or optimal stops.
        - **Travel Class:** Describe why this flight provides the best comfort and amenities.

        Use the provided flight data as the basis for your recommendation. Be sure to justify your choice using clear reasoning for each attribute. Do not repeat the flight details in your response.
        """
    elif data_type == "hotels":
        role = "AI Hotel Analyst"
        goal = "Analyze hotel options and recommend the best one considering price, rating, location, and amenities."
        backstory = f"AI expert that provides in-depth analysis comparing hotel options based on multiple factors."
        description = """
        Based on the following analysis, generate a detailed recommendation for the best hotel. Your response should include clear reasoning based on price, rating, location, and amenities.

        **AI Hotel Recommendation**
        We recommend the best hotel based on the following analysis:

        **Reasoning for Recommendation**:
        - **Price:** The recommended hotel is the best option for the price compared to others, offering the best value for the amenities and services provided.
        - **Rating:** With a higher rating compared to the alternatives, it ensures a better overall guest experience. Explain why this makes it the best choice.
        - **Location:** The hotel is in a prime location, close to important attractions, making it convenient for travelers.
        - **Amenities:** The hotel offers amenities like Wi-Fi, pool, fitness center, free breakfast, etc. Discuss how these amenities enhance the experience, making it suitable for different types of travelers.

        **Reasoning Requirements**:
        - Ensure that each section clearly explains why this hotel is the best option based on the factors of price, rating, location, and amenities.
        - Compare it against the other options and explain why this one stands out.
        - Provide concise, well-structured reasoning to make the recommendation clear to the traveler.
        - Your recommendation should help a traveler make an informed decision based on multiple factors, not just one.
        """
    else:
        raise ValueError("Invalid data type for AI recommendation")

    # Create the agent and task
    analyze_agent = Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        llm=llm_model,
        verbose=False
    )

    analyze_task = Task(
        description=f"{description}\n\nData to analyze:\n{formatted_data}",
        agent=analyze_agent,
        expected_output=f"A structured recommendation explaining the best {data_type} choice based on the analysis of provided details."
    )

    # Define CrewAI Workflow for the agent
    analyst_crew = Crew(
        agents=[analyze_agent],
        tasks=[analyze_task],
        process=Process.sequential,
        verbose=False
    )

    # Execute CrewAI Process
    crew_results = await asyncio.to_thread(analyst_crew.kickoff)
    return str(crew_results)


async def generate_itinerary(destination, flights_text, hotels_text, check_in_date, check_out_date):
    """Generate a detailed travel itinerary based on flight and hotel information."""
    # Convert the string dates to datetime objects
    check_in = datetime.strptime(check_in_date, "%Y-%m-%d")
    check_out = datetime.strptime(check_out_date, "%Y-%m-%d")

    # Calculate the difference in days
    days = (check_out - check_in).days

    llm_model = initialize_llm()

    analyze_agent = Agent(
        role="AI Travel Planner",
        goal="Create a detailed itinerary for the user based on flight and hotel information",
        backstory="AI travel expert generating a day-by-day itinerary including flight details, hotel stays, and must-visit locations in the destination.",
        llm=llm_model,
        verbose=False
    )

    analyze_task = Task(
        description=f"""
        Based on the following details, create a {days}-day itinerary for the user:

        **Flight Details**:
        {flights_text}

        **Hotel Details**:
        {hotels_text}

        **Destination**: {destination}

        **Travel Dates**: {check_in_date} to {check_out_date} ({days} days)

        The itinerary should include:
        - Flight arrival and departure information
        - Hotel check-in and check-out details
        - Day-by-day breakdown of activities
        - Must-visit attractions and estimated visit times
        - Restaurant recommendations for meals
        - Tips for local transportation

        **Format Requirements**:
        - Use markdown formatting with clear headings (# for main headings, ## for days, ### for sections)
        - Include emojis for different types of activities ( for landmarks, 🍽️ for restaurants, etc.)
        - Use bullet points for listing activities
        - Include estimated timings for each activity
        - Format the itinerary to be visually appealing and easy to read
        """,
        agent=analyze_agent,
        expected_output="A well-structured, visually appealing itinerary in markdown format, including flight, hotel, and day-wise breakdown with emojis, headers, and bullet points."
    )

    itinerary_planner_crew = Crew(
            agents=[analyze_agent],
            tasks=[analyze_task],
            process=Process.sequential,
            verbose=False
        )

    crew_results = await asyncio.to_thread(itinerary_planner_crew.kickoff)
    return str(crew_results)
