# Spring Mass Quest

A gamified educational simulation of spring-mass-damping systems that teaches physics through interactive gameplay.

## Overview

Spring Mass Quest is a 2D educational game that demonstrates the physics of spring-mass-damping systems using the fundamental equation:

**M(d²x/dt²) + b(dx/dt) + kx = F(t)**

Where:
- M = Mass
- b = Damping coefficient  
- k = Spring constant
- F(t) = Applied force
- x = Displacement from equilibrium

## Game Features

### 4 Progressive Levels

1. **Level 1: Basic Parameter Adjustment**
   - Learn how mass and damping affect system behavior
   - Goal: Make the system jump higher by adjusting parameters

2. **Level 2: Earthquake Simulation**
   - Case study: Minimize building oscillation during earthquakes
   - Goal: Achieve stable, low-amplitude oscillations

3. **Level 3: Car Suspension**
   - Advanced challenge: Optimize for smooth ride over bumpy roads
   - Goal: Balance comfort and stability

4. **Level 4: Bridge Resonance**
   - Master level: Calculate spring energy to prevent catastrophic failure
   - Goal: Reach specific energy thresholds while maintaining stability

### Interactive Controls

- **Q/W**: Adjust mass
- **A/S**: Adjust damping coefficient
- **Z/X**: Adjust spring constant
- **E/R**: Adjust applied force
- **R**: Reset simulation
- **ESC**: Return to home screen
- **SPACE**: Start game
- **N**: Next level (when level complete)

### Real-time Physics

- Live visualization of spring-mass system
- Real-time parameter adjustment
- Energy calculations (spring, kinetic, total)
- Position, velocity, and acceleration tracking

## Installation

1. Install Python 3.7 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

```bash
python spring_mass_quest.py
```

## Educational Value

This game teaches:
- Understanding of harmonic motion
- Effect of mass on system inertia
- Role of damping in oscillation control
- Spring constant's impact on frequency
- Energy conservation in oscillating systems
- Real-world applications of spring-mass systems

## Game Mechanics

- **Horizontal 2D visualization** for easier understanding
- **Progressive difficulty** across 4 levels
- **Real-time feedback** on system behavior
- **Case study approach** for practical learning
- **Energy calculations** for advanced understanding

## Technical Details

- Built with Pygame for graphics and user interaction
- NumPy for mathematical calculations
- Euler integration for physics simulation
- 60 FPS smooth animation
- Real-time parameter adjustment with immediate visual feedback

Enjoy learning physics through interactive gameplay!