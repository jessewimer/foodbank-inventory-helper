# Foodbank Inventory Helper

A Python application designed to help foodbank staff and volunteers quickly determine recommended shelf life for various food items. This tool provides an easy-to-use interface for looking up consume-by guidelines for shelf-stable, frozen, and refrigerated foods.

## Features

- **Food Item Search**: Search for specific food items to get instant shelf life recommendations
- **Category Browse**: Browse food by categories (shelf-stable, frozen, refrigerated)
- **Interactive Flowchart**: Step-by-step guidance through questions to determine appropriate storage and shelf life
- **Storage Type Support**: Covers all three main storage types:
  - Shelf-stable foods
  - Frozen foods
  - Refrigerated foods

## Purpose

This application helps foodbank operations by:
- Reducing food waste through proper storage guidance
- Ensuring food safety with accurate shelf life information
- Streamlining inventory management processes
- Providing quick reference for volunteers and staff

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/jessewimer/foodbank-inventory-helper.git
   ```

2. Navigate to the project directory:
   ```bash
   cd foodbank-inventory-helper
   ```

3. Install required dependencies (not implemented yet)
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main application:
```bash
python fb_main.py
```

### Search Functionality
- Enter a food item name in the search box
- View recommended shelf life and storage instructions
- Get specific guidance for different storage conditions

### Flowchart Mode
- Answer a series of simple questions about your food item
- Receive customized storage recommendations
- Learn about proper handling and storage conditions

## File Structure

- `fb_main.py` - Main application file
- `food_data.py` - Food database and shelf life data
- `assets/` - Images and UI resources
- `todo.txt` - Development notes and feature requests

## Contributing

This project is designed to serve foodbank communities. If you have suggestions for additional food items, corrections to shelf life data, or feature improvements, please feel free to:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Data Sources

Shelf life recommendations are based on food safety guidelines from:
1. “Shelf Life of Food Bank Products.” 2012. Greater Pittsburgh Community Food Bank
2. “Food Product Dating.” December 2016. USDA Food Safety and Inspection Service.
3. “Bottled Water Storage”. International Bottled Water Association
www.bottledwater.org
4. “Food Storage”; No. EC446; Albrecht, Julie A.; University of Nebraska;
5. “Safe Home Food Storage”; Van Laanen, Peggy; Texas A&M Extension Service; B-
5031; May 1999.
6. “The Food Keeper – A Consumer Guide to Food Quality & Safe Handling.” Food
Marketing Institute.
7. “Classification of Visible External Can Defects”. AOAC International in Cooperation
with the Food and Drug Administration.
8. The Produce Blue Book.
https://www.producebluebook.com/wp-content/uploads/KYC/Fresh-Cut-
Produce.pdf
9. University of California Postharvest Center; http://postharvest.ucdavis.edu/;
http://postharvest.ucdavis.edu/Commodity_Resources/Fact_Sheets/

## License

This project is open source and available for use by foodbank organizations and related community services.

## Support

For questions or support, please open an issue on GitHub or contact the maintainer.

---

*Built to support foodbank operations and reduce food waste in our communities.*