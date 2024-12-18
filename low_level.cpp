#include <Eigen/Dense>
#include <cpr/cpr.h>
#include <iostream>
#include <nlohmann/json.hpp>
#include <time.h>

using json = nlohmann::json;

int main() {
  try {
    // URL cible pour récupérer une tâche
    std::string get_url = "http://127.0.0.1:8000";

    while (true) {
      // Envoyer une requête HTTP GET pour récupérer une tâche
      cpr::Response get_response = cpr::Get(cpr::Url{get_url});

      // Vérifier la réponse
      if (get_response.status_code == 200) {
        std::cout << "Tâche reçue avec succès!" << std::endl;

        // Convertir la réponse en JSON
        json received_json = json::parse(get_response.text);

        // Afficher le JSON reçu
        // std::cout << "JSON reçu : " << received_json.dump(4) << std::endl;

        // Extraire les attributs pour effectuer le calcul
        auto a_data =
            received_json["a"].get<std::vector<std::vector<double>>>();
        auto b_data = received_json["b"].get<std::vector<double>>();

        // Conversion en Eigen::MatrixXd et Eigen::VectorXd
        size_t rows = a_data.size();
        size_t cols = a_data[0].size();

        Eigen::MatrixXd A(rows, cols);
        for (size_t i = 0; i < rows; ++i) {
          for (size_t j = 0; j < cols; ++j) {
            A(i, j) = a_data[i][j];
          }
        }

        Eigen::VectorXd B =
            Eigen::Map<Eigen::VectorXd>(b_data.data(), b_data.size());

        // Résoudre le système linéaire Ax = b
        clock_t t1 = clock();
        Eigen::VectorXd X = A.colPivHouseholderQr().solve(B);
        clock_t t2 = clock();
        double time = (double)(t2 - t1) / CLOCKS_PER_SEC;

        // Afficher les résultats
        // std::cout << "Résultat X : \n" << X << std::endl;

        // Ajouter le vecteur résultat au JSON existant
        received_json["x"] = std::vector<double>(X.data(), X.data() + X.size());
        received_json["time"] = time;

        // Envoyer les résultats via une requête POST
        cpr::Response post_response =
            cpr::Post(cpr::Url{get_url},
                      cpr::Header{{"Content-Type", "application/json"}},
                      cpr::Body{received_json.dump()});

        // Vérifier la réponse du POST
        if (post_response.status_code == 200) {
          std::cout << "Résultats envoyés avec succès!" << std::endl;
        } else {
          std::cerr << "Erreur lors de l'envoi des résultats : "
                    << post_response.status_code << std::endl;
        }
      } else {
        std::cerr << "Erreur lors de la récupération de la tâche : "
                  << get_response.status_code << std::endl;
      }
    }
  } catch (const std::exception &e) {
    std::cerr << "Exception : " << e.what() << std::endl;
  }

  return 0;
}
