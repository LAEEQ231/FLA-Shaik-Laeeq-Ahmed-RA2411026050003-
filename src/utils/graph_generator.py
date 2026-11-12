import os
from graphviz import Digraph

# Dynamically find the absolute path to the assets/diagrams folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIAGRAMS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'assets', 'diagrams'))

def ensure_diagrams_folder():
    """Creates the assets/diagrams folder if it doesn't exist."""
    if not os.path.exists(DIAGRAMS_DIR):
        os.makedirs(DIAGRAMS_DIR)
        print(f"Created directory: {DIAGRAMS_DIR}")

def build_email_graph(highlight_state=None, filename="email_dfa"):
    dot = Digraph(comment='Email DFA', format='png')
    
    # Smaller, cleaner layout
    dot.attr(rankdir='LR', size='7,4', dpi='200')
    
    states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'Dead State / Error']
    
    for s in states:
        shape = 'doublecircle' if s == 'q5' else 'circle'
        fillcolor = 'lightgreen' if s == 'q5' else '#C1292E' if s == 'Dead State / Error' else 'white'
        style = 'filled' if fillcolor != 'white' else ''
        
        if s == highlight_state:
            style = 'filled'
            fillcolor = '#F1D302'
            
        node_id = 'Dead' if s == 'Dead State / Error' else s
        label = f"{s}\n(Accept)" if s == 'q5' else "Dead" if node_id == 'Dead' else s
        if s == 'q0': label += "\n(Start)"
        
        dot.node(node_id, label, shape=shape, style=style, fillcolor=fillcolor, fontsize='11')
        
    # Main path only; repeated chars stay in place (self-loops omitted for clarity)
    dot.edge('q0', 'q1', label=' letter/num ')
    dot.edge('q1', 'q2', label=' @ ')
    dot.edge('q2', 'q3', label=' letter/num ')
    dot.edge('q3', 'q4', label=' . ')
    dot.edge('q4', 'q5', label=' letter/num ')
    dot.edge('q1', 'Dead', label=' . ')
    dot.edge('q2', 'Dead', label=' @/. ')
    
    # Save directly into src/assets/diagrams/
    save_path = os.path.join(DIAGRAMS_DIR, filename)
    dot.render(save_path, cleanup=True)

def build_password_graph(highlight_state=None, filename="password_dfa"):
    dot = Digraph(comment='Password DFA', format='png')
    
    # Smaller, cleaner layout
    dot.attr(rankdir='LR', size='7,4', dpi='200')
    
    states = ['q0', 'q_U', 'q_L', 'q_D', 'q_UL', 'q_UD', 'q_LD', 'q_ULD', 'Rejected']
    
    for s in states:
        shape = 'doublecircle' if s == 'q_ULD' else 'circle'
        fillcolor = 'lightgreen' if s == 'q_ULD' else '#C1292E' if s == 'Rejected' else 'white'
        style = 'filled' if fillcolor != 'white' else ''
        
        if s == highlight_state:
            style = 'filled'
            fillcolor = '#F1D302'
            
        label = f"{s}\n(Accept)" if s == 'q_ULD' else s
        if s == 'q0': label += "\n(Start)"
        
        dot.node(s, label, shape=shape, style=style, fillcolor=fillcolor, fontsize='11')
        
    # Only the transitions that move to a new state (self-loops omitted for clarity)
    dot.edge('q0', 'q_U', label=' U ')
    dot.edge('q0', 'q_L', label=' L ')
    dot.edge('q0', 'q_D', label=' D ')
    dot.edge('q_U', 'q_UL', label=' L ')
    dot.edge('q_U', 'q_UD', label=' D ')
    dot.edge('q_L', 'q_UL', label=' U ')
    dot.edge('q_L', 'q_LD', label=' D ')
    dot.edge('q_D', 'q_UD', label=' U ')
    dot.edge('q_D', 'q_LD', label=' L ')
    dot.edge('q_UL', 'q_ULD', label=' D ')
    dot.edge('q_UD', 'q_ULD', label=' L ')
    dot.edge('q_LD', 'q_ULD', label=' U ')
            
    # Save directly into src/assets/diagrams/
    save_path = os.path.join(DIAGRAMS_DIR, filename)
    dot.render(save_path, cleanup=True)

def build_atm_pin_graph(highlight_state=None, filename="atm_pin_dfa"):
    dot = Digraph(comment='ATM PIN DFA', format='png')
    
    # Smaller, cleaner layout
    dot.attr(rankdir='LR', size='7,3', dpi='200')
    
    states = ['q0', 'q1', 'q2', 'q3', 'q4', 'Dead State / Error']
    
    labels = {'q0': 'q0\n(Start)', 'q1': 'q1\n(1 digit)', 'q2': 'q2\n(2 digits)',
              'q3': 'q3\n(3 digits)', 'q4': 'q4\n(Accept)'}
    
    for s in states:
        shape = 'doublecircle' if s == 'q4' else 'circle'
        fillcolor = 'lightgreen' if s == 'q4' else '#C1292E' if s == 'Dead State / Error' else 'white'
        style = 'filled' if fillcolor != 'white' else ''
        
        if s == highlight_state:
            style = 'filled'
            fillcolor = '#F1D302'
            
        node_id = 'Dead' if s == 'Dead State / Error' else s
        label = "Dead" if node_id == 'Dead' else labels.get(s, s)
        
        dot.node(node_id, label, shape=shape, style=style, fillcolor=fillcolor, fontsize='11')
        
    # Each digit (0-9) advances exactly one state toward acceptance
    dot.edge('q0', 'q1', label=' digit ')
    dot.edge('q1', 'q2', label=' digit ')
    dot.edge('q2', 'q3', label=' digit ')
    dot.edge('q3', 'q4', label=' digit ')
    
    # Any non-digit or 5th digit goes to the dead state (shown once for clarity)
    dot.edge('q0', 'Dead', label=' non-digit ')
    dot.edge('q4', 'Dead', label=' 5th digit ', style='dashed', color='#7f8c8d', fontcolor='#7f8c8d')
    
    # Save directly into src/assets/diagrams/
    save_path = os.path.join(DIAGRAMS_DIR, filename)
    dot.render(save_path, cleanup=True)

if __name__ == "__main__":
    ensure_diagrams_folder()
    
    print(f"Saving files to: {DIAGRAMS_DIR}\n")
    
    print("Generating High-Res Email DFA frames...")
    build_email_graph(filename="email_dfa_base")
    for state in ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'Dead State / Error']:
        safe_name = state.replace(" / ", "_").replace(" ", "_")
        build_email_graph(highlight_state=state, filename=f"email_dfa_{safe_name}")
        
    print("Generating High-Res Password DFA frames...")
    build_password_graph(filename="password_dfa_base")
    for state in ['q0', 'q_U', 'q_L', 'q_D', 'q_UL', 'q_UD', 'q_LD', 'q_ULD', 'Rejected']:
        build_password_graph(highlight_state=state, filename=f"password_dfa_{state}")
        
    print("Generating High-Res ATM PIN DFA frames...")
    build_atm_pin_graph(filename="atm_pin_dfa_base")
    for state in ['q0', 'q1', 'q2', 'q3', 'q4', 'Dead State / Error']:
        safe_name = state.replace(" / ", "_").replace(" ", "_")
        build_atm_pin_graph(highlight_state=state, filename=f"atm_pin_dfa_{safe_name}")
        
    print("\nSuccess! High resolution connected animation frames generated in src/assets/diagrams.")