# PROJECT 1 FOR APAD #

The goal of this project was to create the framework for an event-planning web application. In this part, we developed the basic data model in SQL for storing out application's data and included python utility functions to manipulate the data. We'll be focusing on designing a meeting-room booking in the UT campus. 

## Points of Interest ##
 1. Users: people who use the application
 2. Venues: places where meetings may be planned
 3. Events: events that are currently planned

## Business Rules ## 
 1. The admin manages the site and is able to do operations that the user doesn't have permission for
 2. Users come to events
 3. Venues are available in timeslots of 1-hr during contiguous operating time
 4. A user can start an event at a particular venue at a specific timeslot by specifying a description and capacity
 5. Events are at a venue for a timeslot and have a capacity
 6. A user can join an event if there is enough room

## Operations ##
 1. Add a user (admin only)
 2. Add a new venue (admin only)
 3. Start an event (user or admin on behalf of a user)
 4. Display timeslot availability
 5. Display all venues where a particular timeslot is available
 6. List events at a venue given date/time
 7. Join an event 
 8. Remove an event (admin only) 
