
## Orchestrator
	- Responsible for creating the root agent.
	- Runs the root agent. 

## Modules

Singletons that maintain per-agent state.

### Model
	- Responsible for making the actual model calls.
	- Returns a fixed model response scheme
	- Also maintains per agent config about the model that the agent uses.

### Context
	- Maintains the system, identity, chat and current prompt.
	- Assembles the different sections to get a single prompt

### Tools
	- Executes tools and returns their responses.
	- Makes sure an agent has enough permissions to execute the task.

### Permission
	- Maintains permission of an agent.
	- Escalate the permission of an agent.

## Interface
	- The user facing interface.

## Agent
	- The agent class which is simply an handle.
	- The agent builder which builds agents from files.


## Design Choices

### Should I move the state of agent to the agent itself or have it stored in the modules?
	- If agent keeps it's own state:
		- A bit coupled architecture, agent now needs to know everything.
		- Updating becomes a bit hard since what if the model needs to be updated?
	- If each module keeps the agent's state:
		- We no longer care about each module's implementation.
		- Modules become API like

> Both. Agent context is held by the agent. Tools and permissions by their respective managers.

### Singleton modules or not.
	The only reason the modules are singleton in the first place was that I wanted the Tools module to directly call the Permissions module without
	indirection. 
	Architecturally speaking, it doesn't matter. Because only one instance of each module should exist. The problem is just syntactic.

	- Singleton:
		- Unit testing becomes an absolute hell.
		- It feels a bit brittle.
		- Any module can easily call any other module which is really useful for Permissions or for say Context module to get the string form of the tools available to an agent from Tools module.
	- Non Singleton:
		- Unit testing becomes a bit easier since we can dependancy inject mock modules instead of the real ones.
		- It feels too strict and a lot of dependancy injection to make this work.

> Not singletons.

### Multiple Agents

Every agent needs the ability to summon child agents. This is useful for specific tasks or for doing multiple tasks.
For example, root agent can spawn an agent and tell him to code a complex shell script while it remains active to the user. 

This is a bit complex to implement. 
- Obviously because we are letting something that the orchestrator does, be done by a lower level agent.
- One more problem is how the agents talk to eachother. I was thinking of using the `Interface`.
	- Interface could actually just be another module which kinda makes sense.
	- Each agent can have its own interface. The root agent has the Terminal or User interface while child agents get a AgentInterface which allows them to talk to the parent agent.

> This could definetly work with the Interface idea but first, we need to decide on the first two choices.

### Interfaces

Should interfaces be modules or no?
- Why modules?
	- Because it would allow other modules to talk to the interface directly, allowing us to make update statuses and other stuff.
- Why not?
	- Well I don't really have any reason to not make them modules. Other than the fact that how do we set the first interface? Later on we could have multiple interfaces like GUI, TUI, CLI or even a server.
	
> Made them a high level component. Final diagram at the end.

### OR 

how about we get out of the 'modules' architecture because modules are supposed to be things that have similar responsibilities!

#### Model Manager
This should be global! One model manager that dictates and uses the model each agent requires.

#### Context Manager
This should be per agent. This should also be the main memory model of an agent.

#### Tools
This should also be global. One point of execution. Each model's capabilities are tracked here.

#### Permissions
Also makes sense for this to be global.



# Updated Arch

[Orchestrator] ----v
                   v
[Interface] <-> [Agent] <-> [Model]
				   ^
				   v
				[Tools]

- Interface: Interaction between the agent and the user.
- Agent: The main agent object. Handles control flow and context.
- Model: Global manager responsible for making model calls.
- Tools: Global manager for tool parsing and execution.
- Orchestrator: The class that just boots up the root agent, the interface and the global managers.


# Features that need to be implemented.

- Model Switching: Both automatic and manual. This requires:
	- BaseModel object and supporting multiple models.
	- Each model should get its own class. For example, it would be much easier for each of google's models to have their own classes.

- Commands:
	- Needed for model switching
	- For switching agents
	- Spawning new agents
	- Much more.

- Better Interface:
	- Interface somehow needs to be able to accept the list of commands
	- Also have the ability to be updated and show status like "Thinking..."
	- Display errors
	- Display state and context

- Tools:
	- ToolManager for loading and managing tools
	- ToolBox for keeping the tools
	- ToolExecutor class that handles the execution of tools
	- Tools
		- The absolute best way to parse tools would be to use decorators. Tools would be one-off functions so no need to maintain state between them
		- Just make a box = ToolBox.newBox(); @box.tool() and then ToolBox.giveBox(box)
		- Tools can be just python functions.

- Better prompts:
	- Improved SYSTEM prompt
	- IDENTITY needs more fields:
		- name
		- personality
		- behavior
		- constraints
	- CONTEXT field for context about, well everything.
		- model being used.
		- current working directory
		- current mode
		- current goal
		- tools available
	- HISTORY
		- Condensed chat into history. 
		- Implement this later on.
		- Divided by "events"
	- CHAT
		- Conversational history
		- Divided by roles.
	- PROMPT
		- source mentioned like user, permission, tools.
		- the main message
