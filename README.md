# Disruption Index: Quantifying Shape-Breaking Actions in Football

The **Disruption Index** is a football analytics metric that quantifies how individual player actions—passes, carries, or off-ball movements—disrupt the opposing team’s defensive structure. Unlike traditional metrics like xT or xG, which focus on direct attacking output, the Disruption Index measures the **underlying chaos** that often precedes those moments.

## Why It Matters

Many players exert massive influence without scoring or assisting. They:
- Stretch the back line
- Pull midfielders out of position
- Break compact defensive blocks

The Disruption Index helps analysts and coaches capture these **non-obvious value contributors**.

## How It Works

The model uses spatiotemporal tracking data to quantify changes in team shape following an action. Key metrics include:

- **Δ Width / Height** – Change in defensive team’s spread (meters)
- **Δ Compactness** – Change in spatial density (e.g., mean distance from centroid)
- **Recovery Time** – Time (in seconds) it takes for defensive shape to return to pre-action compactness threshold
- **Composite Disruption Score** – Aggregates shape deltas and recovery duration

Each action is scored based on the magnitude and duration of disruption it causes, normalized across context.

## Core Insight

Disruption Index captures what happens *before* expected threat increases. It can help identify:
- Players who create structural openings
- Possession sequences that generate chaos
- Tactical vulnerabilities in defensive systems

## Example Use Case

> A central midfielder receives the ball under pressure and carries diagonally toward the right channel.  
> → Opponent’s back line shifts and expands by +7.8m  
> → Midfield compactness increases  
> → Recovery time: 6.2s  
> → No shot follows, but the defense is disorganized for the next two possessions  
> → High Disruption Index, xT = 0.  
> → Player credited for structure-breaking impact missed by other metrics.

## Installation

```bash
git clone https://github.com/your-username/disruption-index.git
cd disruption-index
pip install -r requirements.txt
