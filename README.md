# Light-Painting-Newton-s-Rings

<img width="758" alt="b5e7cd9ecaeadcc7a97e0ba34af039b" src="https://github.com/user-attachments/assets/0034f8b4-fa97-4913-93c8-98e7dccb882e" />

---

**Light Painting Newton’s Rings V1.0** is an educational tool designed to simulate the phenomenon of Newton’s rings interference. The interface is cleanly divided into four key sections: **theoretical formulas**, **schematic diagrams**, **dynamic charts**, and **parameter controls**, enabling users to intuitively understand interference principles and observe parameter effects.  

### **Theoretical Formulas Section**  
The left panel displays the radius calculation formulas for bright and dark rings:  
- **Bright ring radius**:  
 
  <img width="184" alt="newton_rings_3_1" src="https://github.com/user-attachments/assets/82af962c-8f94-424c-9536-3fb3cbe531a7" />

- **Dark ring radius**:  
  <img width="161" alt="newton_rings_3_2" src="https://github.com/user-attachments/assets/e734707f-cd85-415c-ac63-e33bced5c194" />

Here, \( k \) is the fringe order, \( λ \) the wavelength, \( R \) the lens curvature radius, and \( d \) the air gap thickness. Users can dynamically validate these formulas by adjusting parameters.  

### **Schematic and Dynamic Charts**  
The top section illustrates the light path and experimental setup (e.g., plano-convex lens and glass plate contact), clarifying how the air film forms. The right side features two interactive charts:  
1. **Intensity distribution**: A graph showing light intensity variation along the radius, where peaks (bright rings) and troughs (dark rings) alternate.  
2. **Interference pattern**: A real-time simulation of concentric Newton’s rings, with vivid color contrasts reflecting parameter changes.  

### **Parameter Controls and Functional Buttons**  
The **"Adjust parameters"** section allows customization of experimental conditions:  
- **Wavelength (λ)**: Adjusts incident light (400–700 nm), altering fringe spacing.  
- **Curvature radius (R)**: Modifies ring density.  
- **Refractive indices (n1/n2/n3)**: Sets values for glass, air gap, and lower glass to manipulate optical path differences.  
- **Actual distance (e)**: Controls air gap thickness (μm), shifting fringe orders.  

Three functional buttons are provided:  
- **Restore default**: Resets all parameters.  
- **Save image**: Exports charts or interference patterns.  
- **Principle document**: Opens detailed theoretical guides.  

By integrating formulas, visuals, and interactive controls, the interface offers a hands-on exploration of Newton’s rings interference, ideal for optics education and experiment preparation.  

Simulation and Analysis of Newton's Rings Interference Phenomenon Based on PyQt5 and Matplotlib，研究成果真正审稿中

---  

### Third-Party Library Requirements (Python 3.9)

### Core Dependencies
| Library       | Version Requirement | Compatibility Notes         |
|---------------|---------------------|-----------------------------|
| PyQt5         | 5.15.9              | Fully compatible with Python 3.9 |
| matplotlib    | 3.7.1               | Requires numpy>=1.21        |
| numpy         | 1.24.3              | Latest stable version supporting Python 3.9 |

### Installation Command
```bash
pip install PyQt5==5.15.9 matplotlib==3.7.1 numpy==1.24.3
