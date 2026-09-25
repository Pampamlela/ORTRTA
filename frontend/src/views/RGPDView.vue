<script setup>
import PageContainer from '@/components/PageContainer.vue';
</script>

<template>
    <PageContainer>
        <div class="prose max-w-none prose-headings:font-title prose-headings:text-film prose-p:text-film prose-li:text-film prose-strong:text-film prose-th:text-film prose-td:text-film">

            <h1>Politique de confidentialité</h1>

            <section>
                <h2>1. Introduction</h2>
                <p>
                    La présente politique de confidentialité décrit la manière dont les données personnelles sont
                    collectées, utilisées et protégées dans le cadre de l'utilisation de l'application
                    One Roll To Rule Them All (www.oneroll.fr).
                </p>
            </section>

            <section>
                <h2>2. Données collectées</h2>
                <p>Nous collectons uniquement les données nécessaires au fonctionnement du service :</p>

                <h3>Données de compte</h3>
                <ul>
                    <li>Adresse e-mail</li>
                    <li>Nom d'utilisateur·ice (username)</li>
                    <li>Mot de passe (jamais stocké en clair : il est haché avant d'être enregistré)</li>
                </ul>

                <h3>Données liées à l'utilisation</h3>
                <ul>
                    <li>Informations sur les pellicules (nom, type, ISO, dates, description)</li>
                    <li>Informations sur le matériel (appareils photo, objectifs, montures)</li>
                    <li>Photos associées aux pellicules (URLs)</li>
                </ul>

                <h3>Données techniques</h3>
                <ul>
                    <li>
                        Journaux d'activité (logs) : nom d'utilisateur·ice, action effectuée (connexion, création,
                        modification ou suppression d'un élément…), date et heure
                    </li>
                </ul>
            </section>

            <section>
                <h2>3. Finalités et base légale</h2>
                <p>Les données sont collectées uniquement pour les finalités suivantes :</p>
                <ul>
                    <li>Création et gestion de votre compte utilisateur·ice</li>
                    <li>Authentification et sécurité</li>
                    <li>Gestion et suivi de vos pellicules photographiques</li>
                    <li>Organisation de votre matériel photo</li>
                    <li>Génération de statistiques personnelles</li>
                </ul>
                <p>
                    Ces traitements reposent sur l'<strong>exécution du contrat</strong> (article 6.1.b du RGPD) :
                    ils sont nécessaires pour vous fournir le service auquel vous vous êtes inscrit·e.
                </p>
                <p>
                    Les journaux d'activité reposent sur notre <strong>intérêt légitime</strong>
                    (article 6.1.f du RGPD) : assurer la sécurité de l'application et diagnostiquer les erreurs.
                </p>
                <p>Aucune donnée n'est collectée à des fins commerciales ou publicitaires.</p>
            </section>

            <section>
                <h2>4. Accès aux données et destinataires</h2>
                <p>Vos données sont accessibles uniquement :</p>
                <ul>
                    <li>par vous-même, via votre compte utilisateur·ice ;</li>
                    <li>par l'administratrice de l'application, uniquement en cas de nécessité technique ou de support.</li>
                </ul>
                <p>
                    Pour faire fonctionner le service, nous faisons appel à des <strong>sous-traitants</strong>,
                    qui traitent vos données uniquement pour notre compte et selon nos instructions :
                </p>
                <ul>
                    <li>
                        <strong>Scaleway</strong> (hébergement) : l'ensemble des données de l'application, y compris
                        les sauvegardes, est hébergé sur des serveurs situés à Paris (France). Aucun transfert hors de
                        l'Union européenne.
                    </li>
                    <li>
                        <strong>Resend</strong> (envoi d'e-mails) : lorsque vous demandez la réinitialisation de votre
                        mot de passe, votre adresse e-mail, votre nom d'utilisateur·ice et le lien de réinitialisation
                        sont transmis à Resend pour l'envoi de l'e-mail. Resend est situé aux États-Unis. Ce transfert
                        est encadré par le <em>Data Privacy Framework</em> UE–États-Unis (décision d'adéquation de la
                        Commission européenne du 10 juillet 2023), auquel Resend est certifié, ainsi que par un accord
                        de traitement des données (DPA).
                    </li>
                </ul>
                <p>Vos données ne sont jamais vendues, ni transmises à des tiers à des fins commerciales ou publicitaires.</p>
            </section>

            <section>
                <h2>5. Durée de conservation</h2>
                <ul>
                    <li>
                        <strong>Données de compte et d'utilisation</strong> : conservées tant que votre compte est
                        actif. Les comptes inactifs depuis plus de <strong>2 ans</strong> après la dernière connexion
                        peuvent être supprimés, avec l'ensemble des données associées.
                    </li>
                    <li>
                        <strong>Journaux d'activité</strong> : conservés dans un volume limité, puis automatiquement
                        écrasés par les plus récents (rotation des fichiers).
                    </li>
                    <li>
                        <strong>Sauvegardes</strong> : conservées 8 jours maximum, puis automatiquement supprimées.
                    </li>
                </ul>
            </section>

            <section>
                <h2>6. Sécurité des données</h2>
                <p>Nous mettons en œuvre des mesures de sécurité pour protéger vos données :</p>
                <ul>
                    <li>Échanges chiffrés via HTTPS</li>
                    <li>Mots de passe hachés avec un algorithme robuste (PBKDF2), jamais stockés en clair</li>
                    <li>Jetons de connexion à durée de vie limitée</li>
                    <li>Contrôle d'accès strict : chaque utilisateur·ice n'accède qu'à ses propres données</li>
                </ul>
            </section>

            <section>
                <h2>7. Vos droits</h2>
                <p>Conformément au RGPD, vous disposez des droits suivants :</p>
                <ul>
                    <li>Droit d'accès : consulter vos données</li>
                    <li>Droit de rectification : modifier vos informations</li>
                    <li>Droit à l'effacement : supprimer votre compte et vos données</li>
                    <li>Droit à la portabilité : récupérer vos données (export)</li>
                    <li>Droit à la limitation du traitement</li>
                </ul>
                <p>
                    Les droits d'accès, de rectification, d'effacement et de portabilité peuvent être exercés
                    directement depuis votre profil dans l'application. Pour toute autre demande, vous pouvez nous
                    contacter à l'adresse indiquée dans la section « Contact ».
                </p>
                <p>
                    Si vous estimez que vos droits ne sont pas respectés, vous pouvez introduire une réclamation
                    auprès de la <strong>CNIL</strong> (Commission nationale de l'informatique et des libertés) :
                    <a href="https://www.cnil.fr" target="_blank" rel="noopener noreferrer">www.cnil.fr</a>.
                </p>
            </section>

            <section>
                <h2>8. Suppression des données</h2>
                <p>La suppression de votre compte entraîne la suppression de l'ensemble de vos données personnelles :</p>
                <ul>
                    <li>Données de compte</li>
                    <li>Pellicules</li>
                    <li>Matériel</li>
                    <li>Photos associées</li>
                </ul>
                <p>Cette action est irréversible.</p>
                <p>
                    Vos données peuvent toutefois subsister dans nos sauvegardes techniques pendant
                    <strong>8 jours maximum</strong> après la suppression de votre compte, avant d'être
                    définitivement effacées. Votre nom d'utilisateur·ice peut également figurer dans les journaux
                    d'activité jusqu'à leur écrasement automatique.
                </p>
            </section>

            <section>
                <h2>9. Cookies et traceurs</h2>

                <h3>Qu'est-ce qu'un cookie ou un traceur ?</h3>
                <p>
                    Un cookie est un petit fichier texte déposé sur votre terminal (ordinateur, tablette, smartphone)
                    lors de la visite d'un site. Plus largement, on parle de <strong>traceur</strong> pour toute
                    information stockée ou lue sur votre terminal, quelle que soit la technologie utilisée
                    (cookies, <em>localStorage</em>, etc.).
                </p>
                <p>
                    Les traceurs peuvent avoir différentes finalités : faire fonctionner le site, mesurer l'audience,
                    afficher de la publicité… Seuls ceux qui sont <strong>strictement nécessaires</strong> au
                    fonctionnement du service sont dispensés de consentement.
                </p>

                <h3>Les traceurs utilisés sur notre site</h3>
                <p>
                    One Roll To Rule Them All utilise <strong>uniquement des traceurs strictement nécessaires</strong>,
                    qui servent à vous authentifier et à maintenir votre connexion :
                </p>
                <table>
                    <thead>
                        <tr>
                            <th>Nom</th>
                            <th>Technologie</th>
                            <th>Finalité</th>
                            <th>Durée de validité</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>access</code></td>
                            <td>localStorage</td>
                            <td>Vous identifier auprès du serveur à chaque action sur le site</td>
                            <td>60 minutes</td>
                        </tr>
                        <tr>
                            <td><code>refresh</code></td>
                            <td>localStorage</td>
                            <td>Renouveler votre connexion sans ressaisir votre mot de passe</td>
                            <td>1 jour</td>
                        </tr>
                    </tbody>
                </table>
                <p>
                    Ces informations sont supprimées de votre navigateur lorsque vous vous déconnectez, ou
                    automatiquement lorsque votre session expire. Si vous fermez simplement le site sans vous
                    déconnecter, elles restent dans votre navigateur, mais deviennent inutilisables une fois leur
                    durée de validité dépassée.
                </p>
                <p>
                    L'administratrice du site utilise également deux cookies techniques (<code>sessionid</code> et
                    <code>csrftoken</code>) lors de l'accès à l'interface d'administration. Ils ne concernent pas
                    les utilisateur·ices du site.
                </p>

                <h3>Pourquoi aucun consentement ne vous est demandé</h3>
                <p>
                    Conformément à l'article 82 de la loi Informatique et Libertés et aux recommandations de la CNIL,
                    les traceurs strictement nécessaires à la fourniture d'un service demandé par l'utilisateur·ice
                    (ici, la connexion à votre compte) sont exemptés de consentement.
                </p>
                <p>
                    One Roll To Rule Them All n'utilise <strong>aucun</strong> traceur de mesure d'audience, de
                    publicité, de réseaux sociaux ou de services tiers. C'est pourquoi aucun bandeau de consentement
                    n'est affiché.
                </p>

                <h3>Comment supprimer ces informations</h3>
                <ul>
                    <li><strong>Depuis le site</strong> : cliquez sur « Déconnexion » ; les deux traceurs sont immédiatement supprimés.</li>
                    <li>
                        <strong>Depuis votre navigateur</strong> : vous pouvez à tout moment effacer les données de
                        navigation (rubrique « Cookies et données de site » des paramètres de votre navigateur).
                    </li>
                </ul>
            </section>

            <section>
                <h2>10. Modification de la politique</h2>
                <p>
                    Cette politique de confidentialité peut être mise à jour à tout moment. En cas de modification
                    importante, les utilisateur·ices seront informé·es.
                </p>
            </section>

            <section>
                <h2>11. Contact</h2>
                <p>
                    Pour toute question relative à cette politique ou à vos données personnelles, vous pouvez
                    contacter : <a href="mailto:pampamlela@gmail.com">pampamlela@gmail.com</a>
                </p>
            </section>

            <section>
                <h2>12. Responsable du traitement</h2>
                <p>La responsable du traitement des données est : Pamela Robinet Duverger.</p>
            </section>

            <p><em>Dernière mise à jour : septembre 2026</em></p>
        </div>
    </PageContainer>
</template>
