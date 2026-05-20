# FoodBridge AI ERD

This ERD represents the core database schema for FoodBridge AI.

## Main Entities

- USERS
- DONATIONS
- NGOS
- CLAIMS
- FOOD_ITEMS

## Relationships

- One User can create many Donations
- One User can have one NGO profile
- One Donation can have many Claims
- One NGO can create many Claims
- Many Donations can belong to one FoodItem category

## Notes

- Role-based access implemented using USERS.role
- Claims system uses state transitions
- ML features integrated through FOOD_ITEMS and freshness_score