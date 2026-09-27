import streamlit as st
from datetime import date
from fpdf import FPDF
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="LegalTech PAI", page_icon="⚖️", layout="centered")

# --- MOTEUR JURIDIQUE EXPERT ---
def generer_corps(enfant, allergene, etape, forme, recours, motifs, type_refus, modalite_medicale, cada_options):
    objet = ""
    doc = ""
    
    if etape == "PREVENTIF":
        objet = f"Prise en charge PAI - {allergene} pour {enfant}"
        doc += "Madame, Monsieur,\n\n"
        doc += f"Je vous fais parvenir ce jour le Projet d'Accueil Individualisé (PAI) de mon enfant, {enfant}, validé et complété par notre médecin spécialiste, nécessitant une stricte éviction liée aux allergènes suivants : {allergene}.\n\n"
        doc += "Conformément à la circulaire interministérielle n° 2021-025 du 10 février 2021 relative au PAI pour raison de santé, l'accueil en restauration scolaire d'un enfant atteint de troubles de la santé doit être garanti et organisé.\n\n"
        doc += "Par ailleurs, l'article L. 131-13 du Code de l'éducation dispose que l'inscription à la cantine est un droit pour tous les enfants scolarisés, sans qu'aucune discrimination ne puisse être établie.\n\n"
        
        if "Plateaux industriels" in modalite_medicale:
            doc += "Dans le cadre des prescriptions de notre médecin spécialiste, la solution privilégiée pour la restauration est la fourniture par la collectivité de plateaux industriels garantis sans allergènes (traces comprises), évitant toute manipulation complexe en cuisine centrale.\n\n"
        elif "Panier-repas" in modalite_medicale:
            doc += "Dans le cadre des prescriptions de notre médecin spécialiste, la solution du panier-repas de substitution est ouverte, sous réserve de la mise en place par vos services du stockage au froid et de la remise à température réglementaire.\n\n"
        else:
            doc += "Le médecin prescripteur a validé plusieurs solutions alternatives sécurisées (plateaux industriels ou panier-repas) afin de garantir l'inclusion de mon enfant.\n\n"
            
        doc += "Je me tiens à votre entière disposition pour échanger sur la mise en œuvre logistique de cette modalité."

    elif etape == "REFUS":
        objet = f"Mise en demeure - Prise en charge PAI de {enfant}"
        doc += "Madame, Monsieur,\n\n"
        
        if forme == "ORAL":
            doc += f"Suite à mes récentes démarches, vos services m'ont indiqué verbalement un refus concernant la prise en charge des repas de {enfant}.\n\n"
            doc += "Or, l'article L. 211-2 du Code des relations entre le public et l'administration (CRPA) impose de motiver formellement les décisions qui refusent un avantage dont l'attribution constitue un droit. Ce refus ne peut donc être formulé qu'à l'écrit, en étant motivé en droit et en fait.\n\n"
            doc += "Afin de me permettre d'exercer mes droits, je vous demande de bien vouloir m'adresser une notification officielle de ce refus. Dans l'attente, je vous prie d'agréer mes salutations distinguées."
            return objet, doc

        doc += f"Par courrier en date du {date.today().strftime('%d/%m/%Y')}, vous m'avez notifié un refus concernant la prise en charge des repas pour {enfant}.\n\n"
        
        if recours == "NON":
            doc += "Je relève tout d'abord que votre décision omet de mentionner les voies et délais de recours. En application de l'article R. 421-5 du Code de justice administrative (CJA), cette omission me permet légalement de contester votre décision sans condition de délai.\n\n"
        
        if "FINANCE" in motifs:
            if type_refus == "TOTAL":
                doc += "Vous motivez ce refus d'accès par un prétexte budgétaire. Or, subordonner l'accès au service public de la restauration (garanti par l'art. L. 131-13 du Code de l'éducation) à un critère de rentabilité lié à l'état de santé de l'enfant caractérise une discrimination prohibée par l'article 225-1 du Code pénal.\n\n"
            else:
                doc += "Vous tentez de rejeter unilatéralement la charge de la restauration sur la famille en refusant d'assurer la fourniture de repas adaptés (tels que les plateaux industriels sécurisés). Cette pratique, qui consiste à imposer le panier-repas par défaut pour éluder vos obligations d'organisation du service public et fuir vos responsabilités financières auprès de votre prestataire, constitue un manquement caractérisé.\n\n"
        
        if "TECHNIQUE" in motifs:
            if type_refus == "TOTAL":
                doc += "Votre justification d'ordre logistique est juridiquement inopérante pour refuser l'accès. Le principe d'adaptation du service public vous commande de trouver les moyens de garantir l'accueil.\n\n"
            else:
                doc += "Votre justification technique est irrecevable. Des solutions externalisées sécurisées (tels que les plateaux industriels scellés) suppriment tout risque de contamination croisée et ne nécessitent aucune charge technique lourde en cuisine centrale.\n\n"
        
        if "MODALITE" in motifs:
            doc += "Vous arguez que la modalité de fourniture du repas ne figure pas formellement dans le modèle type Cerfa de PAI. Ce motif est infondé. La circulaire interministérielle n° 2021-025 impose un devoir d'aménagement global fondé sur l'avis du médecin spécialiste.\n\n"
        
        if type_refus == "TOTAL":
            doc += "Par la présente, je vous mets formellement en demeure de procéder à l'inscription de mon enfant sous huit jours. À défaut, je saisirai le Défenseur des Droits ainsi que la juridiction administrative compétente."
        else:
            doc += "Par la présente, je vous mets formellement en demeure de respecter vos obligations d'organisation du service public en assurant la fourniture de repas sécurisés adaptés, faute de quoi je formerai un recours pour excès de pouvoir (REP) devant le Tribunal Administratif."

    elif etape == "CADA":
        objet = "Demande de communication de documents administratifs (Restauration)"
        doc += "Madame, Monsieur,\n\n"
        doc += f"Face à votre refus persistant concernant la prise en charge des repas de {enfant}, et afin de préparer les suites contentieuses de ce dossier, je sollicite formellement la communication des documents administratifs suivants :\n"
        doc += "- Le contrat de marché public ou de concession de restauration collective vous liant à votre prestataire actuel (CCAP et CCTP intégraux).\n"
        doc += "- Le Bordereau des Prix Unitaires (BPU) ainsi que ses éventuels avenants.\n"
        doc += "- Le ou les devis écrits attestant de vos démarches formelles auprès de prestataires spécialisés pour évaluer le coût de repas adaptés ou de plateaux industriels garantis sans allergènes.\n"
        
        if "CLAUSES" in cada_options:
            doc += "- Les extraits précis du cahier des charges (CCTP) encadrant les obligations du prestataire en matière de gestion des régimes alimentaires particuliers et des PAI.\n"
        if "ECHANGES" in cada_options:
            doc += "- L'ensemble des échanges écrits (e-mails, courriers, comptes-rendus) entre vos services et votre prestataire de restauration concernant les demandes d'aménagement de repas pour les enfants allergiques.\n"
        if "PIECES" in cada_options:
            doc += "- Les éventuels règlements intérieurs ou cahiers des charges spécifiques applicables aux structures d'accueil périscolaire et de restauration de la collectivité.\n"

        doc += "\nEn application de l'article L. 311-1 du Code des relations entre le public et l'administration (CRPA), toute personne a le droit d'obtenir communication des documents administratifs (au sens de l'art. L. 300-2 du même code) détenus par une administration.\n\n"
        doc += "En l'absence de réponse favorable de votre part dans un délai strict d'un mois, je saisirai la Commission d'Accès aux Documents Administratifs (CADA) pour faire valoir mon droit."

    elif etape == "DDD":
        objet = f"Saisine - Droit à la scolarisation inclusive et accès cantine ({enfant})"
        doc += "Madame, Monsieur le Délégué du Défenseur des Droits,\n\n"
        doc += f"Je vous saisis afin de dénoncer une situation de rupture d'égalité et de mise à l'écart dont est victime mon enfant, {enfant}, souffrant d'une pathologie nécessitant une éviction stricte ({allergene}).\n\n"
        doc += "La collectivité refuse d'appliquer les modalités de restauration préconisées par le médecin spécialiste dans le cadre du PAI (circulaire n° 2021-025), méconnaissant l'intérêt supérieur de l'enfant (Convention internationale des droits de l'enfant, art. 3-1) et l'article L. 131-13 du Code de l'éducation.\n\n"
        doc += "Le refus systématique de prendre en charge la fourniture matérielle des repas en rejetant la charge logistique sur la famille crée une rupture d'égalité de fait en pénalisant les enfants porteurs de PAI.\n\n"
        doc += "Face à l'inaction de la collectivité malgré mes mises en demeure, je vous demande d'intervenir et d'instruire ce dossier afin de rétablir mon enfant dans ses droits fondamentaux."

    return objet, doc

def generer_pdf_bytes(nom, adresse, ville, collectivite, enfant, objet, corps):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 11)
    
    def txt(texte):
        return texte.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.set_xy(15, 20)
    pdf.multi_cell(80, 5, txt=txt(f"{nom}\n{adresse}\n{ville}"))
    pdf.set_xy(110, 35)
    pdf.multi_cell(85, 5, txt=txt(f"À l'attention de :\n{collectivite}"))
    pdf.set_xy(110, 60)
    ville_seule = ville.split(" ", 1)[-1] if " " in ville else ville
    pdf.cell(85, 5, txt=txt(f"Fait à {ville_seule}, le {date.today().strftime('%d/%m/%Y')}"))
    pdf.set_xy(15, 80)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 5, txt=txt(f"Objet : {objet}"))
    pdf.set_font("Arial", "", 11)
    pdf.set_xy(15, 100)
    pdf.multi_cell(0, 6, txt=txt(corps), align="J")
    pdf.ln(15)
    pdf.set_x(130)
    pdf.cell(0, 5, txt=txt("Signature :"))
    
    pdf.output("temp_courrier.pdf")
    with open("temp_courrier.pdf", "rb") as f:
        bytes_data = f.read()
    return bytes_data


# --- INTERFACE WEB STREAMLIT ---
st.markdown("<h1 style='text-align: center;'>⚖️ 🍽️ RIPOSTE PAI</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-size: 1.3rem; color: #333;'>Projet d'Accueil Individualisé</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size: 1.0rem; color: #555;'>Assistant administratif pour faire valoir vos droits dans le cadre de l'instauration du PAI au sein de la restauration collective des écoles</h3>", unsafe_allow_html=True)

# MANIFESTE CITOYEN (Directement visible - Texte exact d'origine)
st.markdown("#### 📢 Pourquoi cet outil ? Lisez notre manifeste")
st.markdown("""
**Cette plateforme est née d'une initiative citoyenne. Elle a une vocation strictement gratuite et désintéressée : vous réarmer face à l'administration en vous informant de vos droits.**

En tant que citoyens, nous avons des devoirs envers l'administration. Mais n'oublions jamais que nous avons aussi des droits. Trop souvent, l'administration oublie jusqu'au Code qui régit sa propre profession et les règles qui encadrent ses relations avec ses administrés.

Dans le parcours du combattant qu'est la mise en place d'un Projet d'Accueil Individualisé (PAI) pour votre enfant, on vous opposera presque systématiquement deux arguments : *"c'est trop cher"* ou *"c'est trop compliqué"*. 

**Mais posez-vous cette question :** lorsque cette même administration vous somme de payer une facture d'eau, une redevance poubelle ou des taxes locales, vous permettez-vous de répondre que *"c'est trop cher"* ou *"trop compliqué"* ? Vous payez, et c'est tout. Et si vous ne le faites pas, rassurez-vous, l'administration n'aura aucun scrupule à vous envoyer des rappels et à mandater une société de recouvrement s'il le faut pour recouvrer votre dette. 

L'exigence de respect de la loi doit être réciproque. Ne vous laissez plus faire. Ne laissez plus vos enfants sans prise en charge par la collectivité. 

Un enfant soumis à un PAI strict a le droit fondamental de bénéficier du **même service public intégral** que ses camarades. Les prétentions tarifaires d'un prestataire privé, comme Sodexo ou Elior, ne sauraient pénaliser un jeune administré, ni le renvoyer – par simple défaut de volonté politique – à une gamelle réchauffée de la veille. 

C'est précisément la mission, et l'intérêt même, d'une collectivité territoriale de faire valoir son poids d'acheteur public pour négocier des tarifs d'éviction raisonnables, et de défendre l'égalité absolue de tous ses administrés.

**Face aux refus abusifs, ne baissez plus les bras. Utilisez le droit.**
""")

# NOTE RGPD SÉCURITÉ & DISCLAIMER JURIDIQUE
st.caption("🔒 **Confidentialité & RGPD :** Ce site est un outil citoyen qui ne collecte et ne stocke aucune donnée personnelle. Les informations saisies ci-dessous (noms, adresses, pathologies) sont uniquement utilisées temporairement pour générer votre document PDF et sont immédiatement supprimées.")

st.warning("""
⚠️ **Avertissement et conditions d'utilisation :**
* **Riposte PAI** est un outil d'assistance technique et d'information citoyenne bénévole. Il ne constitue en aucun cas une consultation juridique formalisée ni un service d'avocat.
* Les modèles générés s'appuient sur les textes officiels en vigueur, mais leur adaptation et leur envoi relèvent de l'entière responsabilité de l'utilisateur. 
* L'auteur de l'outil ne pourra en aucun cas être tenu responsable de l'usage fait des documents générés ni des suites administratives ou contentieuses données par les collectivités.
""")

st.markdown("---")

st.write("### 1. Vos coordonnées")
col1, col2 = st.columns(2)
with col1:
    var_nom = st.text_input("Nom et Prénom", "Jean Dupont")
    var_ville = st.text_input("Code postal & Ville", "75000 Paris")
with col2:
    var_adresse = st.text_input("Adresse postale", "1 place de l'Hôtel de Ville")

st.write("### 2. Le dossier")
col3, col4 = st.columns(2)
with col3:
    var_enfant = st.text_input("Prénom de l'enfant", "Léo")
    var_allergene = st.text_input("Allergies / Pathologie", "Allergie à l'arachide, fruits à coques, sésame")
with col4:
    var_collectivite = st.text_input("Destinataire (Collectivité, Com-com...)", "Nom de l'administration compétente")

var_modalite_medicale = st.selectbox(
    "Modalité de restauration prescrite par le médecin (PAI / Certificat)",
    (
        "Plateaux industriels garantis sans allergènes (traces comprises)",
        "Panier-repas fourni par la famille",
        "Les deux solutions (au choix / selon organisation)"
    )
)

st.write("### 3. La stratégie juridique")
etape = st.selectbox(
    "Quelle démarche souhaitez-vous effectuer ?",
    (
        "PREVENTIF - Dépôt du dossier PAI", 
        "REFUS - Mettre en demeure l'administration (collectivité territoriale...)", 
        "CADA - Exiger les contrats", 
        "DDD - Saisir le Défenseur des Droits"
    )
)
code_etape = etape.split(" ")[0]

var_forme = "ECRIT"
var_recours = "OUI"
coute_cher = False
complique = False
modalite_non_inscrite = False
type_refus = "TOTAL"
cada_options = []

if code_etape == "REFUS":
    var_forme = st.radio("Comment l'administration a-t-elle formulé son refus ?", ("ORAL", "ECRIT"))
    
    if var_forme == "ECRIT":
        st.markdown("---")
        type_refus = st.radio(
            "Quelle est la nature exacte du refus ?", 
            ("TOTAL : L'administration refuse tout accès à la cantine (l'enfant est renvoyé chez lui le midi)", 
             "PARTIEL : L'administration accepte l'enfant mais refuse de fournir les repas adaptés (imposition abusive du panier-repas)")
        )
        if "TOTAL" in type_refus: type_refus = "TOTAL"
        else: type_refus = "PARTIEL"
        
        st.markdown("---")
        var_recours = st.radio("Le courrier de refus indique-t-il les voies et délais de recours à la fin ?", ("OUI", "NON"))
        st.write("Quelles excuses ont-ils donné dans le courrier ?")
        coute_cher = st.checkbox("Ça coûte trop cher")
        complique = st.checkbox("C'est trop compliqué à gérer logistiquement")
        modalite_non_inscrite = st.checkbox("La modalité n'est pas inscrite dans le formulaire PAI")

elif code_etape == "CADA":
    st.write("Précisions complémentaires à exiger (optionnel) :")
    if st.checkbox("Exiger les clauses du CCTP relatives aux régimes alimentaires et PAI"):
        cada_options.append("CLAUSES")
    if st.checkbox("Exiger les échanges écrits / e-mails entre la collectivité et le prestataire"):
        cada_options.append("ECHANGES")
    if st.checkbox("Exiger les règlements intérieurs applicables aux cantines"):
        cada_options.append("PIECES")

st.markdown("---")

# Création d'une mémoire pour le bouton générer
if "apercu_genere" not in st.session_state:
    st.session_state.apercu_genere = False

if st.button("Générer l'aperçu du courrier"):
    st.session_state.apercu_genere = True

# L'aperçu ne s'affiche que si le bouton a été cliqué au moins une fois
if st.session_state.apercu_genere:
    motifs = []
    if coute_cher: motifs.append("FINANCE")
    if complique: motifs.append("TECHNIQUE")
    if modalite_non_inscrite: motifs.append("MODALITE")

    objet, corps = generer_corps(var_enfant, var_allergene, code_etape, var_forme, var_recours, motifs, type_refus, var_modalite_medicale, cada_options)

    st.write("### 📝 Aperçu de votre courrier :")
    st.info(f"**Objet :** {objet}\n\n{corps}")

    # CONSEIL JURIDIQUE LRAR
    st.warning("⚠️ **CONSEIL D'ENVOI :** L'envoi par courrier électronique (e-mail) est parfois suffisant. Toutefois, pour vous prémunir contre la mauvaise foi administrative (e-mail prétendument perdu, spam, mauvais service...), il est **fortement recommandé** d'envoyer ce courrier en **Lettre Recommandée avec Accusé de Réception (LRAR)** ou de le remettre en main propre contre décharge. C'est le seul moyen incontestable de faire courir les délais légaux.")

    pdf_bytes = generer_pdf_bytes(var_nom, var_adresse, var_ville, var_collectivite, var_enfant, objet, corps)

    st.download_button(
        label="⬇️ Télécharger le PDF prêt à envoyer",
        data=pdf_bytes,
        file_name=f"Courrier_PAI_{var_enfant}.pdf",
        mime="application/pdf",
        type="primary"
    )
