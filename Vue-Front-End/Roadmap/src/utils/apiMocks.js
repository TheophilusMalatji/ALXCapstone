// src/utils/apiMocks.js
// Clean Promise-based mock API used by the app (replaces Gemini's malformed mocks)

const mockRoadmaps = [
  {
    id: 1,
    title: "Frontend Developer Roadmap",
    description: "Learn HTML, CSS, JS, frameworks and tooling.",
    levels: [
      { id: 1, title: "HTML & CSS Basics", status: "complete" },
      { id: 2, title: "JavaScript Fundamentals", status: "in-progress" },
      { id: 3, title: "Framework (Vue/React) Basics", status: "todo" }
    ]
  },
  {
    id: 2,
    title: "Backend Developer Roadmap",
    description: "APIs, databases, auth & deployment.",
    levels: [
      { id: 1, title: "Node.js Basics", status: "complete" },
      { id: 2, title: "Databases", status: "todo" }
    ]
  }
];

const mockProfile = {
  id: 1,
  name: "Jane Developer",
  role: "Product Engineer",
  stats: {
    roadmapsCompleted: 2,
    activeRoadmaps: 1,
    xp: 4200
  }
};

/**
 * Simulate network latency (optional).
 * @param {any} value
 * @param {number} [ms=250]
 */
const withDelay = (value, ms = 200) =>
  new Promise((resolve) => setTimeout(() => resolve(value), ms));

export const fetchRoadmaps = async () => {
  // Return a copy to avoid accidental mutation
  return withDelay(JSON.parse(JSON.stringify(mockRoadmaps)));
};

export const fetchRoadmapById = async (id) => {
  const roadmap = mockRoadmaps.find((r) => Number(r.id) === Number(id));
  return withDelay(roadmap ? JSON.parse(JSON.stringify(roadmap)) : null);
};

export const fetchProfile = async () => {
  return withDelay(JSON.parse(JSON.stringify(mockProfile)));
};
