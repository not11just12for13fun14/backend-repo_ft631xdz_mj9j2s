"""
Database Schemas for Boccone Restaurant

Each Pydantic model represents a collection in MongoDB.
Class name (lowercased) becomes the collection name.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class Dish(BaseModel):
    """
    Menu items (mainly pasta). Collection: "dish"
    """
    name: str = Field(..., description="Dish name")
    description: Optional[str] = Field(None, description="Short description")
    category: str = Field("pasta", description="Category: pasta, sauce, topping, extra")
    price: float = Field(..., ge=0, description="Price in EUR")
    tags: List[str] = Field(default_factory=list, description="Tags like vegan, spicy, gluten-free")
    image: Optional[str] = Field(None, description="Public image URL if any")
    featured: bool = Field(False, description="Whether to show in highlights")


class Reservation(BaseModel):
    """
    Guest reservations. Collection: "reservation"
    """
    name: str = Field(..., description="Guest full name")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: str = Field(..., description="Contact phone")
    date: str = Field(..., description="Reservation date (YYYY-MM-DD)")
    time: str = Field(..., description="Reservation time (HH:MM)")
    guests: int = Field(..., ge=1, le=20, description="Number of guests")
    notes: Optional[str] = Field(None, description="Special requests")


class BocconeBuild(BaseModel):
    """
    A custom first-course build composed of small bites (bocconi). Collection: "bocconebuild"
    """
    title: str = Field(..., description="User-given name for the build")
    items: List[str] = Field(..., description="List of dish IDs or names included")
    price: float = Field(..., ge=0, description="Computed price")
    customer_name: Optional[str] = Field(None, description="Optional name of creator")
    created_at: Optional[datetime] = None
