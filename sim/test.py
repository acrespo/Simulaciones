import unittest

from models import Company, Workflow, Project

class WorkflowTest(unittest.TestCase):

    def test_empty(self):

        w = Workflow(20, 0, [])
        self.assertTrue(w.is_deliverable())
        self.assertEqual(w.average_workload(), 0)

    def test_add(self):

        w = Workflow(20, 0, [])
        self.assertEqual(w.projects, [])

        p = Project(20, 1, 3)
        new_w = w.add_project(p)

        self.assertNotEqual(w, new_w)
        self.assertEqual(new_w.projects, [p])
        self.assertEqual(w.projects, [])

    def test_workload(self):

        p1 = Project(30, 1, 3)
        p2 = Project(30, 1, 3)

        w = Workflow(20, 0, [p1, p2])

        self.assertEqual(w.average_workload(), 3)

        w.reserved_resources = 4
        self.assertAlmostEqual(w.average_workload(), 3.75)

        p3 = Project(30, 1, 3)
        p3.hours_left = 5

        w2 = w.add_project(p3)
        self.assertAlmostEqual(w2.average_workload(), 4.0625)

        w3 = Workflow(20, 20, [])
        self.assertEqual(w3.average_workload(), 0)

        w4 = Workflow(20, 20, [p1, p2])
        self.assertEqual(w4.average_workload(), 0)

    def test_deliverable_without_reserved(self):
        p1 = Project(300, 1, 3)
        p2 = Project(300, 1, 3)

        w = Workflow(4, 0, [p1, p2])

        self.assertTrue(w.is_deliverable())

        w2 = w.add_project(Project(300, 1, 3))
        self.assertFalse(w2.is_deliverable())

        w.resources = 3
        self.assertFalse(w.is_deliverable())

    def test_deliverable_with_reserved(self):
        p1 = Project(300, 1, 3)
        p2 = Project(300, 1, 3)

        w = Workflow(4, 2, [p1, p2])

        self.assertFalse(w.is_deliverable())

        w2 = w.add_project(Project(300, 1, 3))
        self.assertFalse(w2.is_deliverable())

        w.resources = 6
        self.assertTrue(w.is_deliverable())

    def test_deliverable_awesome(self):
        self.fail()

    def test_undeliverable_awesome(self):
        self.fail()

    def test_work(self):
        self.fail()

if __name__ == '__main__':
    unittest.main()
