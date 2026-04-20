@echo off 
echo Setting up Othello project... 
mkdir othello 
cd othello 
mkdir src\othello\core src\othello\players src\othello\gui src\othello\utils tests docs 
python -m venv venv 
venv\Scripts\activate 
pip install --upgrade pip 
pip install pytest pytest-cov black flake8 isort pyqt6 sphinx 
echo Setup complete! 