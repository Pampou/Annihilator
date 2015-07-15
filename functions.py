import sfml as sf
import math

def setOriginToCenter(entity):
	entityRect = entity.local_bounds
	entity.origin = sf.Vector2(entityRect.left + entityRect.width/2, entityRect.top  + entityRect.height/2)
	
	return entity
	
def collision(firstEntity, secondEntity, radius = 16):
	x1, y1 = firstEntity.getPos()
	x2, y2 = secondEntity.getPos()
	
	result = math.sqrt(((x1 - x2)*(x1 - x2))+((y1 - y2)*(y1 - y2)))
	
	if result < radius:
		return True
	else:
		return False