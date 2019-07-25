# PROJECT 1 for APAD #

The goal of this project was to create the framework for an event-planning web application. In this part, we developed the basic data model in SQL for storing out application's data and included python utility functions to manipulate the data. We'll be focusing on designing a meeting-room booking in the UT campus. 

## Points of Interest ##
 Markup : 
 1. Users: people who use the application
 2. Venues: places where meetings may be planned
 3. Events: events that are currently planned

## Business Rules ## 
Markup : 
 1. The admin manages the site and is able to do operations that the user doesn't have permission for
 2. Users come to events
 3. Venues are available in timeslots of 1-hr during contiguous operating time


1.2 2. Business Rules
0. Admin manages the site and is able to do operations not permitted to a user
1. Users play in events
2. Venues are available in timeslots of 1-hr during contiguous operating time
3. A user can start an event at a particular venue at a specific timeslot by specifying a description and capacity
4. Events are at a venue for a timeslot and have a capacity
5. A user can join an event if there is room
