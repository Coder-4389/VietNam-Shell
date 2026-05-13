# VietNam Shell 0.0.1 

- VietNam Shell is a CLI had being made by VietNamese
- overcome the limitations in VietNam Shell

- VietNam Shell was have a TUI made by `Customtkinter` 
    + you can install customtkinter with pip by command below
    ```bash
    sudo apt update
    sudo apt install python3-pip
    pip3 install customtkinter
    
    ```

    + you can learn how to use Customtkinter in below link , in that link have all Customtkinter function and way to use those function
    https://customtkinter.tomschimansky.com/

    + Develop VietNam Shell's TUI in `source/view/` or `assets`

---

## Some notes about VietNam Shell you need know before develop

1.  **The structure of project:**
    + The source folder have structure is like this
    ```
    source/
    ├─ runtime/
    ├─ script/
    ├─ view/
    └─ registry.py
    ```

    ---
    > It have 3 main dir are: 
    - **runtime folder is a folder have runtime and write by C or C++.**
    - **script folder is a folder contain analyzer the code's syntax.**
    - **view folder have app TUI and app interface with python's customtkinter**

2. **The language use to do project**
    + The project use 3 main languages are `Python` and `C/C++`.
    + Python use to make the TUI and analyzer because it have a clear syntax and can best support string.
    + C/C++ use to build a compiler and runtime because it can run fastly and it are low-level language.

3. **Buils a community for Shell**
    + You can build a community for VietNam Shell in internet
    + You talking VietNam Shell for more coder to make popularity

---

 ## The steps to move the project and develop environment from github to your computer

 1. **Install git if you don't have**
    ```bash
    sudo apt update
    sudo apt install git
    ```

2. **Download the project from github**
    ```bash
    git clone https://github.com/ten-nguoi-dung/ten-du-an.git
    ```

3. **Make the environment for the project**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4. **Install all library we need to develop**
    ```bash
    pip3 install -r requirements.txt
    ```

- **if you used more library to develop the project**
- **you need write and run** `pip freeze > requirements.txt`
