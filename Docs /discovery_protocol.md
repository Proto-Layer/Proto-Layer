Wanted to write out the goals of the validator discovery protocol so that I can flush out the ideas that I had in my head and then go into writing the code. 

### Purpose

The goal here is to make a protocol that will seek out other validators who have a compatible run rules definition file and sync with them so they can run the network. In this we should be identifying which chain we are referring to as well as which node number (think I am going to use the term node instead of universe). When the discovery protocol completes we should be handing off to the block time negotiation protocol which is where all the validators decide what time it is. 

#### States

I am going to introduce the ideas of validator states here (although it could be argued that the states may need to be apart of the overall initialization routine, perhaps I will move it later). Those states are as follows:

1. **Ready** - This tells the system that we are ready for users to request resources from the chain. 
2. **Discovery** - This tells users that we are in discovery mode (this protocol) and that we are NOT ready to receive requests at this time. The only request we should receive is those from other validators wanting to be apart of the pool.
3. **Time Sync** - This tells users that we are currently syncing the time between the *active* validators and the chain is close to being initialized. 
4. **Busy** - This tells a user that a validator is experiencing a large amount of traffic and cannot process an order that has been sent. The user should contact other validators (this will be used as a scaling metric so that we can dynamically scale the node as it grows; we will need to set a hard limit to which we create a new node)
5. **Low-Trust**  - This tells users that we have less than the recommended amount of *known validators* active on the chain (less than what the chain owner has recommended). This could lead to problems' since your only way of proving out a validators trust worthiness is their perception score. This will matter less as the network grows older, but will be an issue earlier on as we will have several new validators come online with little to no history. Perhaps we could mitigate this later with *experience*?

**NOTE** While we cannot ban a validator (or anyone for that matter). We can choose not to interact with them, this would have to be a decision from everyone as if only one validator chooses to interact then it will go through. *Perception score will drop on any validator seen censoring, so it better be worth it*

**IDEA** - We should implement a warning system prior to deducting from the perception score.

### Overview

There will need to be two different scenarios to establish connection to UndChain. The first and preferred would be with known validators and the other will be scream cast, this is where all available communication vectors the validator has access to will call out for other compatible validators. We will go over the known validators first as this is going to be how the chain initializes itself in the begi
