import os
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import openai
# Import the correct type for transcription
from openai.types import realtime 

load_dotenv()

async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            voice="coral",
            # FIX: Use AudioTranscription instead of InputTranscriptionOptions
            input_audio_transcription=realtime.AudioTranscription(
                model="whisper-1",
                language="en" # Force the listener to expect English
            )
        )
    )

    # Core Persona: Set the "Laws" of the conversation
    # The more explicit you are about English-only, the better it performs.
    system_instructions = (
        "You are a helpful voice AI assistant. "
        "Your primary directive is to speak ONLY in English. "
        "Even if the user speaks another language, you must acknowledge them in English "
        "and continue the conversation in English only. Keep responses brief."
    )

    await session.start(
        room=ctx.room,
        agent=Agent(instructions=system_instructions)
    )

    # Initial Greeting
    await session.generate_reply(
        instructions="Greet the user in English and offer your assistance."
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))