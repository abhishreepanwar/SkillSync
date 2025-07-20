document.addEventListener('DOMContentLoaded', () => {
  const storedResult = sessionStorage.getItem('resumeResult');
  if (!storedResult) {
    alert('No resume data found. Please analyze a resume first.');
    window.location.href = 'index.html';
    return;
  }

  const resultData = JSON.parse(storedResult);
  displayResumeResults(resultData);
});

function displayResumeResults(data) {
  const resultsSection = document.getElementById('resume-results');

  const similarity = data.similarity_score || 0;
  document.getElementById('similarity-score').textContent = similarity;

  // ✅ Matched Skills
  const matchedSkills = document.getElementById('matched-skills');
  matchedSkills.innerHTML = '';
  (data.matched_skills || []).forEach(skill => {
    const tag = document.createElement('span');
    tag.className = 'skill-tag';
    tag.textContent = skill;
    matchedSkills.appendChild(tag);
  });

  // ✅ Missing Skills
  const missingSkills = document.getElementById('missing-skills');
  missingSkills.innerHTML = '';
  (data.missing_skills || []).forEach(skill => {
    const tag = document.createElement('span');
    tag.className = 'skill-tag missing';
    tag.textContent = skill;
    missingSkills.appendChild(tag);
  });

  // ✅ Improvement Suggestions
  const improvementList = document.getElementById('improvement-suggestions');
  improvementList.innerHTML = '';
  (data.improvement_areas || []).forEach(point => {
    const li = document.createElement('li');
    li.textContent = point;
    improvementList.appendChild(li);
  });

  // 🎯 Doughnut Chart – Match %
  const matchCanvas = document.getElementById('match-chart');
  if (window.matchChart) window.matchChart.destroy();
  window.matchChart = new Chart(matchCanvas, {
    type: 'doughnut',
    data: {
      labels: ['Match %', 'Gap %'],
      datasets: [{
        data: [similarity, 100 - similarity],
        backgroundColor: ['#4CAF50', '#E0E0E0']
      }]
    },
    options: {
      plugins: {
        legend: {
          display: true,
          position: 'bottom'
        }
      },
      cutout: '70%'
    }
  });

  // 📊 Bar Chart – Skill Counts
  const barCanvas = document.getElementById('skill-bar-chart');
  if (window.skillBarChart) window.skillBarChart.destroy();
  window.skillBarChart = new Chart(barCanvas, {
    type: 'bar',
    data: {
      labels: ['Matched Skills', 'Missing Skills'],
      datasets: [{
        label: 'Skill Count',
        data: [
          (data.matched_skills || []).length,
          (data.missing_skills || []).length
        ],
        backgroundColor: ['#2196F3', '#FF7043']
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1 }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });

  resultsSection.classList.remove('hidden');
}
