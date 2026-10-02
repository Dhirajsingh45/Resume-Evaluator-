from models.candidate import Candidate
from models.job import Job

from services.embedding_services import calculate_similarity


SIMILARITY_THRESHOLD = 0.55


def build_candidate_evidence(candidate: Candidate):

    evidence = []

    evidence.extend(candidate.skills)
    evidence.extend(candidate.experience)
    evidence.extend(candidate.projects)
    evidence.extend(candidate.education)
    evidence.extend(candidate.certifications)

    return evidence


def calculate_score(candidate: Candidate, job: Job):

    candidate_evidence = build_candidate_evidence(candidate)

    matched = []
    missing = []

    score = 0

    for requirement in job.requirements:

        best_similarity = 0
        best_evidence = None

        for evidence in candidate_evidence:

            similarity = calculate_similarity(
                requirement.skill,
                evidence
            )

            if similarity > best_similarity:

                best_similarity = similarity
                best_evidence = evidence

        if best_similarity >= SIMILARITY_THRESHOLD:

            matched.append({
                "skill": requirement.skill,
                "weight": requirement.weight,
                "similarity": round(best_similarity, 3),
                "evidence": best_evidence
            })

            score += requirement.weight

        else:

            missing.append({
                "skill": requirement.skill,
                "weight": requirement.weight,
                "similarity": round(best_similarity, 3)
            })

    return {
        "score": score,
        "matched": matched,
        "missing": missing
    }