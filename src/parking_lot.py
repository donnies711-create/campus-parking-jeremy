"""Parking lot management classes"""
from typing import List, Optional
from datetime import datetime


class ParkingSpaceClass:
    """Represents a single parking space"""
    
    def __init__(self, space_id: int, space_number: str, category: str = 'regular'):
        """Initialize a parking space
        
        Args:
            space_id: Unique identifier for the space
            space_number: Space number/label (e.g., 'A-01')
            category: Type of space (regular, accessible, reserved)
        """
        self.space_id = space_id
        self.space_number = space_number
        self.category = category
        self.is_available = True
        self.current_reservation = None
        self.last_updated = datetime.utcnow()
    
    def occupy(self, reservation_id: int) -> bool:
        """Mark space as occupied
        
        Args:
            reservation_id: ID of the reservation occupying this space
            
        Returns:
            True if successful, False if space is not available
        """
        if not self.is_available:
            return False
        self.is_available = False
        self.current_reservation = reservation_id
        self.last_updated = datetime.utcnow()
        return True
    
    def release(self) -> bool:
        """Mark space as available
        
        Returns:
            True if successful, False if already available
        """
        if self.is_available:
            return False
        self.is_available = True
        self.current_reservation = None
        self.last_updated = datetime.utcnow()
        return True
    
    def __repr__(self):
        status = 'Available' if self.is_available else 'Occupied'
        return f'<ParkingSpace {self.space_number} [{self.category}] - {status}>'


class ParkingLotClass:
    """Represents a parking lot with multiple spaces"""
    
    def __init__(self, lot_id: int, name: str, location: str, total_spaces: int):
        """Initialize a parking lot
        
        Args:
            lot_id: Unique identifier for the lot
            name: Name of the parking lot
            location: Location/address of the lot
            total_spaces: Total number of spaces in the lot
        """
        self.lot_id = lot_id
        self.name = name
        self.location = location
        self.total_spaces = total_spaces
        self.spaces: List[ParkingSpaceClass] = []
        self.created_at = datetime.utcnow()
    
    def add_spaces(self, count: int, category: str = 'regular', start_number: int = 1) -> None:
        """Add parking spaces to the lot
        
        Args:
            count: Number of spaces to add
            category: Category of spaces (regular, accessible, reserved)
            start_number: Starting number for space numbering
        """
        for i in range(count):
            space_num = start_number + i
            space_number = f"{self.name[0]}-{space_num:03d}"
            space = ParkingSpaceClass(len(self.spaces) + 1, space_number, category)
            self.spaces.append(space)
    
    def get_available_spaces(self, category: Optional[str] = None) -> List[ParkingSpaceClass]:
        """Get all available spaces in the lot
        
        Args:
            category: Filter by category (optional)
            
        Returns:
            List of available parking spaces
        """
        available = [s for s in self.spaces if s.is_available]
        if category:
            available = [s for s in available if s.category == category]
        return available
    
    def get_space_by_number(self, space_number: str) -> Optional[ParkingSpaceClass]:
        """Get a specific space by its number
        
        Args:
            space_number: The space number to find
            
        Returns:
            ParkingSpace object or None if not found
        """
        for space in self.spaces:
            if space.space_number == space_number:
                return space
        return None
    
    @property
    def available_count(self) -> int:
        """Get count of available spaces"""
        return len(self.get_available_spaces())
    
    @property
    def occupancy_rate(self) -> float:
        """Calculate current occupancy rate
        
        Returns:
            Occupancy percentage (0-100)
        """
        if self.total_spaces == 0:
            return 0
        occupied = self.total_spaces - self.available_count
        return round((occupied / self.total_spaces) * 100, 2)
    
    def get_status(self) -> dict:
        """Get current status of the parking lot
        
        Returns:
            Dictionary with lot status information
        """
        return {
            'lot_id': self.lot_id,
            'name': self.name,
            'location': self.location,
            'total_spaces': self.total_spaces,
            'available_spaces': self.available_count,
            'occupied_spaces': self.total_spaces - self.available_count,
            'occupancy_rate': self.occupancy_rate,
            'created_at': self.created_at
        }
    
    def __repr__(self):
        return f'<ParkingLot {self.name} - {self.available_count}/{self.total_spaces} available>'
