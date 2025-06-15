<?php

/** Adminer configuration for pgVector database auto-connection */

function adminer_object() {

    class AdminerAutoLogin extends Adminer {

        function credentials() {
            // Return database credentials for auto-login
            return array('postgres', 'postgres', 'password');
        }

        function database() {
            // Set default database
            return 'vectordb';
        }

        function login($login, $password) {
            // Auto-login for pgVector database
            if ($login == 'postgres' && $password == 'password') {
                return true;
            }
            return parent::login($login, $password);
        }

        function loginForm() {
            // Pre-fill login form
            echo "<table cellspacing='0'>\n";
            echo "<tr><th>" . lang('System') . "<td>" . html_select("auth[driver]", array("pgsql" => "PostgreSQL"), DRIVER, "loginDriver(this);") . "\n";
            echo "<tr><th>" . lang('Server') . "<td><input name='auth[server]' value='postgres' title='" . lang('hostname[:port]') . "' placeholder='localhost' autocapitalize='off'>\n";
            echo "<tr><th>" . lang('Username') . "<td><input name='auth[username]' id='username' value='postgres' autocomplete='username' autocapitalize='off'>\n";
            echo "<tr><th>" . lang('Password') . "<td><input type='password' name='auth[password]' value='password' autocomplete='current-password'>\n";
            echo "<tr><th>" . lang('Database') . "<td><input name='auth[db]' value='vectordb' placeholder='" . lang('database') . "' autocapitalize='off'>\n";
            echo "</table>\n";
            echo "<p><input type='submit' value='" . lang('Login') . "'>\n";
            echo checkbox("auth[permanent]", 1, $_COOKIE["adminer_permanent"], lang('Permanent login')) . "\n";
        }

        function name() {
            // Custom title
            return 'pgVector Database Admin';
        }

        function css() {
            // Custom CSS for better appearance
            return array('https://www.adminer.org/static/designs/pepa-linha-dark/adminer.css');
        }

        function homepage() {
            // Show helpful information on homepage
            echo "<h3>pgVector Database Management</h3>";
            echo "<p>Welcome to the pgVector database admin panel!</p>";
            echo "<p><strong>Quick Access:</strong></p>";
            echo "<ul>";
            echo "<li><a href='?pgsql=postgres&username=postgres&db=vectordb&select=documents'>View Documents Table</a></li>";
            echo "<li><a href='?pgsql=postgres&username=postgres&db=vectordb&sql='>SQL Query</a></li>";
            echo "<li><a href='?pgsql=postgres&username=postgres&db=vectordb&table=documents'>Table Structure</a></li>";
            echo "</ul>";

            // Show vector extension info
            echo "<h4>pgVector Extension Status</h4>";
            $result = connection()->query("SELECT extname, extversion FROM pg_extension WHERE extname = 'vector'");
            if ($result && $result->num_rows > 0) {
                $row = $result->fetch_assoc();
                echo "<p>✅ pgVector extension is installed (version: " . h($row['extversion']) . ")</p>";
            } else {
                echo "<p>❌ pgVector extension not found</p>";
            }

            // Show document count
            try {
                $result = connection()->query("SELECT COUNT(*) as count FROM documents");
                if ($result && $result->num_rows > 0) {
                    $row = $result->fetch_assoc();
                    echo "<p>📊 Total documents in database: " . h($row['count']) . "</p>";
                }
            } catch (Exception $e) {
                echo "<p>📊 Documents table not yet created</p>";
            }
        }

        function tablesPrint($tables) {
            // Highlight important tables
            echo "<h3>Database Tables</h3>";
            foreach ($tables as $table => $type) {
                if ($table === 'documents') {
                    echo "<p><strong>📄 <a href='" . h(ME) . "select=" . urlencode($table) . "'>" . h($table) . "</a></strong> - Vector documents storage</p>";
                } else {
                    echo "<p><a href='" . h(ME) . "select=" . urlencode($table) . "'>" . h($table) . "</a></p>";
                }
            }
        }
    }

    return new AdminerAutoLogin;
}

include "./adminer.php";
