spot
====

Python based LMS using Django

This is actually my third (or fifth depending on how you count) attempt to build something that is actually 
useful in the management of my class. Originally I wanted something that would make beautiful documents for
class, so I learned LaTeX. Next I wanted to serve them to students via the web, so I learned PHP. I knew that
eventually I wanted to do more, so I learned Python. Then I found Django. After a brief stint with Flask, I
have returned, and I am trying to start this off right.

Really, I want functionality something like Moodle powered by Python. Frankly, I can't believe it doesn't
already exist. I've seen a couple of projects out there, but nothing mature enough for me to abandon what
I've already done on my own. So here we are.

This is my initial set of objectives, each corresponding to a separate app or multiple apps.

1. Minimal course managment system

   - Facilitate placement of course materials online
   - Permission-based restriction of those documents (student-only, instrutor-only)
   - Associating students with courses
   - ? [ Storing student submissions ]
   - ? [ Mediating communication between teachars, students ]

2. Tracking student performance
    
   - Web-based entry of assignments and grades
   - Provide student access to their own grades
   - Export for final calculation or simple record keeping

3. Create and maintain beautiful course materials

   - Support multiple kinds of documents (syllabus, lecture notes, slides, homework, quizzes, labs, projects)
   - Dead simple to update and recreate when necessary
   - Publish in multiple formats, but primarily PDF with LaTeX support

4. Learning management system (LMS)

   - Integrated content/assessment delivery
   - Self-directed learning "shop" (modular)
   - Record learning progress (Tin can API)
    
The first three I have already done some development work on. The fourth is more of a catch-all to keep track of 
things that would be great to add on in the future to turn this project into a true LMS.