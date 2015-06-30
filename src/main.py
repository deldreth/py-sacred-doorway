#!/usr/bin/python

from doorway.doorway import Doorway

sacred = Doorway()

sacred.put(1, 255, 0, 0)
sacred.put(2, 0, 255, 0)
sacred.put(3, 0, 0, 255)
sacred.put(4, 255, 255, 0)
sacred.put(5, 0, 255, 255)
sacred.put(6, 255, 0, 255)
sacred.put(7, 255, 255, 255)
sacred.render()
