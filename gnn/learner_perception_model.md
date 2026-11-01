# GNN Example: Learner Perception Model

# GNN Version: 1.0

# A two-state perception model of the reader of this syllabus: while reading,
# you observe how a term lands, and that observation updates your belief about
# whether the term is already connected to what you know.

## GNNSection

ActInfPOMDP

## GNNVersionAndFlags

GNN v1

## ModelName

Learner Perception Model

## ModelAnnotation

A minimal perception model of the adventure-mode reader:

- 2 hidden states: a notion is either "rooted" (connected to what you already
  know) or "floating" (still unattached)
- 2 observations: the passage either "reads smoothly" or "reads as noise"
- A likelihood matrix A maps hidden states to observations
- A prior D records where you start on a term before you read the passage
- A minimal 2-action transition component B marks two study moves (re-read,
  move on) so the model is a complete POMDP for optional framework rendering;
  perception itself needs no action planning
- Neutral preferences C: the exercise is inference, not reward

## StateSpaceBlock

# Generative model parameters

A[2,2,type=float]    # Likelihood matrix: P(observation | hidden state)
B[2,2,2,type=float]  # Transition matrix: B[next_state, previous_state, action]
C[2,type=float]      # Preference vector over observations
D[2,1,type=float]    # Prior belief over hidden states

# Hidden state

s[2,1,type=float]    # Hidden state (posterior belief)

# Observation

o[2,1,type=int]      # Observation (one-hot encoded)

# Action

u[1,type=int]        # Action taken

## Connections

D>s
s-A
A-o
s-B
B>u
u>s

## InitialParameterization

# A[o,s]: P(reads smoothly | rooted) = 0.85; P(reads as noise | floating) = 0.75

A={
  (0.85, 0.25),
  (0.15, 0.75)
}

# Two study moves. B is stored as (next_state, previous_state, action); per-action
# slices are column-stochastic: action 0 = re-read the passage (drift toward
# rooted), action 1 = move on (drift toward floating).

B={
  ( (0.85, 0.20), (0.15, 0.80) ),
  ( (0.15, 0.80), (0.85, 0.20) )
}

# Neutral preference over observations

C={(0.0, 0.0)}

# Most terms arrive unattached: 0.4 rooted, 0.6 floating

D={(0.4, 0.6)}

## Equations

A[o,s] = P(o | s). For the single observation o, Bayesian perception is
q(s) = D[s] A[o,s] / sum_j D[j] A[o,j]. Equivalently, for one-hot o,
q = softmax(log D + log(A^T o)).

Worked examples with this parameterization:

- "reads smoothly" (o=0): q = (0.34, 0.15) / 0.49 = (0.6939, 0.3061)
- "reads as noise" (o=1): q = (0.06, 0.45) / 0.51 = (0.1176, 0.8824)

The transition component uses B[next,previous,action]. Action 0 re-reads and
drifts toward rooted with probability 0.85; action 1 moves on and drifts toward
floating with probability 0.80. For a chosen action u the predicted next-state
belief is q_next = B[:,:,u] q; an actual next state is sampled according to
P(s_next | s,u) = B[:,s,u]. Neutral C keeps this a perception exercise.

## Time

Static

## ActInfOntologyAnnotation

A=LikelihoodMatrix
B=TransitionMatrix
C=PreferenceVector
D=Prior
s=HiddenState
o=Observation
u=Action

## ModelParameters
b_tensor_order: next_state_previous_state_action

num_hidden_states: 2
num_obs: 2
num_actions: 2
num_timesteps: 2

## Footer

Learner Perception Model v1 - GNN Representation.
Two hidden states, two observations, two study moves.
Written for the Connections unit of the Active Inference & Category Theory syllabus.

## Signature

Cryptographic signature goes here
