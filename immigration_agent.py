import json
import os

# Charger la base de connaissances
with open("knowledge_base.json", "r", encoding="utf-8") as f:
    KNOWLEDGE_BASE = json.load(f)


class ImmigrationAgent:
    def __init__(self):
        self.knowledge = KNOWLEDGE_BASE

    def get_knowledge_context(self):
        """Formate la base de connaissances pour l'injection dans le prompt"""
        context = "Base de connaissances sur l'immigration canadienne:\n"

        # Section Visas
        context += "\n## Visas disponibles:\n"
        for visa in self.knowledge["visas"]:
            context += f"- {visa['type']}: {visa['description']}\n"
            if "eligibility" in visa:
                context += "  Critères d'éligibilité:\n"
                for criterion, description in visa["eligibility"].items():
                    context += f"  • {criterion}: {description}\n"

        # Section Exigences linguistiques
        lang = self.knowledge.get("exigences_linguistiques", {})
        context += "\n## Exigences linguistiques:\n"
        context += f"- Tests acceptés: {', '.join(lang.get('tests_acceptés', {}).get('anglais', []))} (anglais), {', '.join(lang.get('tests_acceptés', {}).get('français', []))} (français)\n"
        context += f"- Validité des tests: {lang.get('validity', '')}\n"

        # Section Biométrie
        bio = self.knowledge.get("biométrie", {})
        context += "\n## Biométrie:\n"
        context += f"- Coût: {bio.get('coût', '')}\n"
        context += f"- Validité: {bio.get('validity', '')}\n"

        return context

    def _find_visa_by_type(self, visa_type):
        """Trouve un visa par son type (insensible à la casse)"""
        for visa in self.knowledge["visas"]:
            if visa["type"].lower() == visa_type.lower():
                return visa
        return None

    def get_visa_types(self):
        """Retourne la liste des types de visas disponibles"""
        return [visa["type"] for visa in self.knowledge["visas"]]

    def get_profile_types(self):
        """Retourne la liste des types de profils disponibles"""
        return ["étudiant", "travailleur", "visiteur", "résident"]

    def get_required_documents(self, visa_type, destination=None):
        """Retourne la liste des documents requis pour un visa"""
        visa = self._find_visa_by_type(visa_type)
        if not visa:
            return ["Type de visa non reconnu"]

        docs = visa.get("documents", [])
        if destination and "québec" in destination.lower():
            docs.append("Certificat d'acceptation du Québec (CAQ)")
        return docs

    def get_eligibility_criteria(self, visa_type):
        """Retourne les critères d'éligibilité pour un visa"""
        visa = self._find_visa_by_type(visa_type)
        if not visa:
            return {}
        return visa.get("eligibility", {})

    def get_processing_time(self, visa_type):
        """Retourne le délai de traitement pour un visa"""
        visa = self._find_visa_by_type(visa_type)
        if not visa:
            return "Information non disponible"
        return visa.get("processing_time", "Information non disponible")

    def get_language_requirements(self, program_name):
        """Retourne les exigences linguistiques pour un programme"""
        requirements = self.knowledge.get("exigences_linguistiques", {})
        return requirements.get("scores_min", {}).get(program_name, {})

    def check_eligibility(self, visa_type, user_profile):
        """Vérifie l'éligibilité préliminaire basée sur le profil utilisateur"""
        visa = self._find_visa_by_type(visa_type)
        if not visa:
            return False, ["Type de visa non reconnu"]

        criteria = visa.get("eligibility", {})
        reasons = []

        # Vérification des critères
        if "age" in criteria and user_profile.age:
            if visa_type == "PVT" and not (18 <= user_profile.age <= 35):
                reasons.append(
                    "Âge non conforme (doit être entre 18 et 35 ans)")

        if "fonds" in criteria and user_profile.funds:
            min_funds = 12500  # Exemple pour permis d'études
            if visa_type == "Permis d'études" and user_profile.funds < min_funds:
                reasons.append(
                    f"Fonds insuffisants (minimum {min_funds} $ CAD)")

        if "nationalité" in criteria and user_profile.nationality:
            if visa_type == "PVT" and user_profile.nationality.lower() not in ["france", "belgique", "suisse"]:
                reasons.append("Nationalité non éligible au PVT")

        return len(reasons) == 0, reasons

    def suggest_visa_options(self, user_profile):
        """Suggère les meilleures options de visa basées sur le profil"""
        suggestions = []
        for visa in self.knowledge["visas"]:
            eligible, _ = self.check_eligibility(visa["type"], user_profile)
            if eligible:
                suggestions.append({
                    "type": visa["type"],
                    "description": visa.get("description", ""),
                    "match_score": self.calculate_match_score(visa, user_profile)
                })

        # Trier par meilleur match
        suggestions.sort(key=lambda x: x["match_score"], reverse=True)
        return suggestions

    def calculate_match_score(self, visa, user_profile):
        """Calcule un score de correspondance entre le visa et le profil utilisateur"""
        score = 0

        # Âge
        if visa["type"] == "PVT" and 18 <= user_profile.age <= 35:
            score += 40

        # Type de profil
        if user_profile.profile_type == "étudiant" and visa["type"] == "Permis d'études":
            score += 30
        elif user_profile.profile_type == "travailleur" and visa["type"] == "Permis de travail":
            score += 30

        # Destination
        if visa["type"] == "Permis d'études" and "québec" in user_profile.destination.lower():
            score += 20

        return score

    def get_official_resources(self, visa_type=None):
        """Retourne les ressources officielles pertinentes"""
        resources = self.knowledge["resources"]["liens_officiels"].copy()

        if visa_type:
            visa = self._find_visa_by_type(visa_type)
            if visa:
                if "Permis d'études" in visa_type:
                    resources["Guide spécifique"] = self.knowledge["resources"]["guides"]["Guide_étude"]
                elif "travail" in visa_type.lower():
                    resources["Guide spécifique"] = self.knowledge["resources"]["guides"]["Guide_travail"]

        return resources
