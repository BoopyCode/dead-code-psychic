#!/usr/bin/env python3
"""Dead Code Psychic - Sees what your IDE can't (and what you wish you couldn't)."""

import ast
import os
import sys
from collections import defaultdict

class DeadCodeMedium:
    """Communicates with the spirit world of unused variables and forgotten functions."""
    
    def __init__(self):
        self.defined_names = defaultdict(set)  # Where code goes to die
        self.used_names = defaultdict(set)     # Where code actually gets used (rare)
        
    def analyze_file(self, filepath):
        """Reads your code's future (spoiler: it's mostly dead)."""
        try:
            with open(filepath, 'r') as f:
                tree = ast.parse(f.read(), filename=filepath)
            
            # Find all the hopeful definitions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self.defined_names[filepath].add(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        self.defined_names[filepath].add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        self.defined_names[filepath].add(alias.name)
                
            # Find what's actually being used (the 10% that matters)
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    self.used_names[filepath].add(node.id)
                elif isinstance(node, ast.Attribute):
                    # Handle module.attribute references
                    if isinstance(node.value, ast.Name):
                        self.used_names[filepath].add(node.value.id)
                        
        except (SyntaxError, UnicodeDecodeError):
            print(f"Psychic blocked by cursed file: {filepath}")
    
    def reveal_dead_code(self):
        """Summons the ghosts of code past."""
        print("\n🔮 DEAD CODE PSYCHIC READING 🔮\n")
        print("I sense... regret... and unused imports...\n")
        
        total_dead = 0
        for filepath in self.defined_names:
            dead = self.defined_names[filepath] - self.used_names[filepath]
            if dead:
                print(f"📁 {os.path.basename(filepath)}:")
                for name in sorted(dead):
                    print(f"   👻 {name} (rest in peace)")
                    total_dead += 1
        
        if total_dead == 0:
            print("Miracle! No dead code found. Are you a wizard?")
        else:
            print(f"\nTotal dead entities: {total_dead} (they're in a better place now)")

def main():
    """Main séance - gather round, children of the code."""
    if len(sys.argv) < 2:
        print("Usage: python dead_code_psychic.py <file_or_directory>")
        print("Example: python dead_code_psychic.py .")
        sys.exit(1)
    
    target = sys.argv[1]
    psychic = DeadCodeMedium()
    
    if os.path.isfile(target) and target.endswith('.py'):
        psychic.analyze_file(target)
    elif os.path.isdir(target):
        for root, _, files in os.walk(target):
            for file in files:
                if file.endswith('.py'):
                    psychic.analyze_file(os.path.join(root, file))
    else:
        print("Psychic confusion: Target must be .py file or directory")
        sys.exit(1)
    
    psychic.reveal_dead_code()

if __name__ == "__main__":
    main()