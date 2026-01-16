"""
Complete example: Create PowerPoint presentation using Anthropic PPTX Skill
Requires: pip install anthropic
Requires: ANTHROPIC_API_KEY environment variable
"""

import anthropic
import os

def create_presentation(topic: str, num_slides: int = 5, output_filename: str = "presentation.pptx"):
    """
    Create a PowerPoint presentation using Anthropic's PPTX Skill.

    Args:
        topic: The topic for the presentation
        num_slides: Number of slides to create
        output_filename: Output file name for the presentation
    """

    # Initialize client (uses ANTHROPIC_API_KEY env var)
    client = anthropic.Anthropic()

    print(f"Creating presentation about: {topic}")
    print(f"Number of slides: {num_slides}")
    print("-" * 50)

    # Step 1: Create the presentation using PPTX skill
    response = client.beta.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=16384,
        betas=["code-execution-2025-08-25", "skills-2025-10-02"],
        container={
            "skills": [
                {
                    "type": "anthropic",
                    "skill_id": "pptx",
                    "version": "latest"
                }
            ]
        },
        messages=[{
            "role": "user",
            "content": f"Create a professional presentation about {topic} with {num_slides} slides. Include a title slide, content slides with key points, and a conclusion slide."
        }],
        tools=[{
            "type": "code_execution_20250825",
            "name": "code_execution"
        }]
    )

    print("Response received. Processing...")

    # Step 2: Extract file ID from response
    file_id = None

    for block in response.content:
        # Print text responses from Claude
        if block.type == "text":
            print(f"\nClaude: {block.text[:500]}..." if len(block.text) > 500 else f"\nClaude: {block.text}")

        # Look for file references in code execution results
        if block.type == "code_execution_tool_result":
            if hasattr(block, 'content'):
                for item in block.content:
                    if hasattr(item, 'type') and item.type == 'file':
                        file_id = item.file_id
                        print(f"\nFound file ID: {file_id}")
                        break

    # Alternative: Check for server_tool_use blocks
    if not file_id:
        for block in response.content:
            if hasattr(block, 'type') and block.type == 'server_tool_use':
                if hasattr(block, 'result') and hasattr(block.result, 'content'):
                    for item in block.result.content:
                        if hasattr(item, 'file_id'):
                            file_id = item.file_id
                            print(f"\nFound file ID: {file_id}")
                            break

    if not file_id:
        # Debug: Print full response structure
        print("\nDebug - Full response content types:")
        for i, block in enumerate(response.content):
            print(f"  Block {i}: type={block.type}")
            if hasattr(block, '__dict__'):
                print(f"    Attributes: {list(block.__dict__.keys())}")

        print("\nNo file was generated. Check the response above for details.")
        return None

    # Step 3: Download the file
    print(f"\nDownloading file...")

    file_content = client.beta.files.download(
        file_id=file_id,
        betas=["files-api-2025-04-14"]
    )

    # Step 4: Save to disk
    with open(output_filename, "wb") as f:
        f.write(file_content.read())

    print(f"\nPresentation saved to: {output_filename}")
    print(f"File size: {os.path.getsize(output_filename) / 1024:.1f} KB")

    return output_filename


def main():
    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nSet it using:")
        print("  Windows: set ANTHROPIC_API_KEY=your-api-key")
        print("  Linux/Mac: export ANTHROPIC_API_KEY=your-api-key")
        return

    # Example: Create a presentation
    topic = "Python Programming Basics"
    output_file = create_presentation(
        topic=topic,
        num_slides=5,
        output_filename="python_basics.pptx"
    )

    if output_file:
        print(f"\nSuccess! Open {output_file} to view your presentation.")


if __name__ == "__main__":
    main()
