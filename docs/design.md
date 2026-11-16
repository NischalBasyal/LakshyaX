# LakshyaX design archive

These are the original LakshyaX mockups and planning diagrams. They show the early design of the product, including ideas that changed during implementation.

## Product screens

| Original mockup | What it shows |
| --- | --- |
| [Add a goal](design-assets/add-goal.png) | Prompts for the goal, requirements, deadline, category, and importance. The early design also explored an hours estimate and a full calendar grid. |
| [View active goals](design-assets/active-goals.png) | Goals stay visible in a grid of category cards, with an update action on each card. The image filenames are placeholders from the mockup. |
| [Points dashboard](design-assets/points-dashboard.png) | A personal welcome and one prominent points total. The original points table awarded 10, 25, or 40 points based on importance. |
| [Completed goals](design-assets/completed-goals.png) | An early layout for reviewing finished goals. The hosted version shows the goal deadline and provides a reflection preview and full-text dialog. |
| [Sign in](design-assets/sign-in.png) | A centered sign-in form. This early mockup used an email field. The app signs in with a username. |
| [Sign up](design-assets/sign-up.png) | A short account-creation form. The implemented form also asks users to confirm their password. |

## Planning diagrams

- [Use cases](design-assets/use-cases.png) and [navigation map](design-assets/navigation-map.png) show how the initial screens and roles fit together. Goal assignment is an early design idea.
- [Sign-up flow](design-assets/signup-flow.png) and [sign-in flow](design-assets/sign-in-flow.png) sketch credential checks and the path into the app.
- [View and update flow](design-assets/view-and-update-flow.png) and [completion flow](design-assets/complete-goal-flow.png) sketch how goals move through the system. The completion sketch shows the early points and removal steps. The app also saves a completed record and its reflection.
- [Early data model](design-assets/data-model.png), [goal field table](design-assets/goal-fields.png), and [points rules](design-assets/points-rules.png) capture the original storage and scoring decisions. The current model includes a completed-goal record and links goals and points to the user.
- [Admin sign-in flow](design-assets/admin-sign-in-flow.png) and [admin portal flow](design-assets/admin-portal-flow.png) document the original administration concepts.

[Back to LakshyaX](../README.md)
