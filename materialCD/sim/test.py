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
        p1 = Project(300, 1, 3)
        p2 = Project(300, 1, 3)

        w = Workflow(6, 2, [p1, p2])
        self.assertTrue(w.is_deliverable())

        awesome = Project(300, 1, 3)
        awesome.is_awesome = True

        w2 = w.add_project(awesome)
        self.assertFalse(w2.is_deliverable())

        awesome.extra_devs = 1
        self.assertFalse(w2.is_deliverable())

        awesome.extra_devs = 2
        self.assertTrue(w2.is_deliverable())


    def test_undeliverable_awesome(self):
        p1 = Project(300, 1, 3)
        p2 = Project(300, 1, 3)

        awesome = Project(300, 1, 3)
        awesome.is_awesome = True
        awesome.extra_devs = 2

        w = Workflow(6, 2, [p1, p2, awesome])
        self.assertTrue(w.is_deliverable())

        not_awesome = Project(300, 1, 3)
        not_awesome.is_awesome = True
        not_awesome.extra_devs = 2

        w2 = w.add_project(not_awesome)
        self.assertFalse(w2.is_deliverable())

    def test_sequential_awesome(self):
        p1 = Project(2 * 480, 1, 2)
        p2 = Project(2 * 480, 1, 2)

        awesome = Project(320, 1, 3)
        awesome.is_awesome = True
        awesome.extra_devs = 2

        w = Workflow(6, 2, [p1, p2, awesome])
        self.assertTrue(w.is_deliverable())

        not_awesome = Project(320, 1, 1)
        not_awesome.is_awesome = True
        not_awesome.extra_devs = 2

        w2 = w.add_project(not_awesome)
        self.assertTrue(w2.is_deliverable())

    def test_parallel_awesome(self):
        p1 = Project(2 * 480, 1, 2)
        p2 = Project(2 * 480, 1, 2)

        awesome = Project(160, 1, 1)
        awesome.is_awesome = True
        awesome.extra_devs = 1

        w = Workflow(6, 2, [p1, p2, awesome])
        self.assertTrue(w.is_deliverable())

        not_awesome = Project(160, 1, 1)
        not_awesome.is_awesome = True
        not_awesome.extra_devs = 1

        w2 = w.add_project(not_awesome)
        self.assertTrue(w2.is_deliverable())

    def test_lots_of_awesome(self):
        p1 = Project(2 * 480, 1, 2)
        p2 = Project(2 * 480, 1, 2)

        awesome = Project(160, 1, 1)
        awesome.is_awesome = True
        awesome.extra_devs = 1

        not_awesome = Project(2 * 160, 1, 1)
        not_awesome.is_awesome = True
        not_awesome.extra_devs = 1

        w = Workflow(7, 3, [p1, p2, awesome, not_awesome])
        self.assertTrue(w.is_deliverable())

        more_awesome = Project(6 * 160, 1, 1)
        more_awesome.periods_to_delivery = 3
        more_awesome.is_awesome = True
        more_awesome.extra_devs = 2

        w2 = w.add_project(more_awesome)
        self.assertFalse(w2.is_deliverable(), msg = "Fails, it need one more dev")

        more_awesome.extra_devs = 3
        self.assertTrue(w2.is_deliverable())


    def test_work(self):
        pass

if __name__ == '__main__':
    unittest.main()
